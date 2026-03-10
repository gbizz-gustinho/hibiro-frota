import os
import logging
from datetime import date
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import get_db 
# Importamos a validação para o alerta do Dashboard
from utils.utils_format import validar_cnpj

# Configurações de Upload
UPLOAD_FOLDER = 'static/uploads/nfs'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

frota_bp = Blueprint('frota', __name__, url_prefix='/frota')

# --- DECORATOR DE SEGURANÇA ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Acesso restrito. Por favor, faça login.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUXILIAR DE MOEDA (MÁSCARA REVERSA) ---
def limpar_moeda(v):
    if not v: return 0.0
    # Limpa "R$ ", pontos e troca vírgula por ponto
    v_limpo = str(v).replace('R$', '').replace('.', '').replace(',', '.').strip()
    return float(v_limpo)

# --------------------------------------------------------------------------
# ROTA: DASHBOARD (COM ALERTA DE CNPJ)
# --------------------------------------------------------------------------
@frota_bp.route('/')
@login_required 
def dashboard():
    conn = get_db()
    usuario_id = session.get('user_id')
    
    # 1. BUSCA O CNPJ DA EMPRESA VINCULADA AO USUÁRIO
    empresa = conn.execute('SELECT CNPJ FROM cad_empresa WHERE id_usuario = ?', (usuario_id,)).fetchone()
    
    # 2. LÓGICA DE TRAVA DO SAAS (A variável que a Sidebar espera)
    # Se o CNPJ for o padrão, vazio ou nulo, o perfil está incompleto
    perfil_completo = False
    if empresa and empresa['CNPJ'] not in ["00000000000000", "", None]:
        perfil_completo = True
    
    # Salva na sessão para que a Sidebar em qualquer página saiba o status
    session['perfil_completo'] = perfil_completo

    # 3. CONTADORES RÁPIDOS
    total_motoristas = conn.execute("SELECT COUNT(*) FROM cad_clifor WHERE tipo_clifor = 'MOTORISTA'").fetchone()[0]
    total_veiculos = conn.execute("SELECT COUNT(*) FROM vei_imobilizado WHERE status_veiculo = 'ATIVO'").fetchone()[0]

    # 4. DADOS PARA GRÁFICOS
    tipos_data = conn.execute('''
        SELECT t.nome_tipo, COUNT(v.id_veiculo) 
        FROM vei_imobilizado v 
        JOIN vei_tipo_carroceria t ON v.id_tipo = t.id_tipo 
        GROUP BY t.nome_tipo
    ''').fetchall()
    
    marcas_data = conn.execute('''
        SELECT m.nome_marca, COUNT(v.id_veiculo) 
        FROM vei_imobilizado v 
        JOIN vei_modelo mo ON v.id_modelo = mo.id_modelo 
        JOIN vei_marca m ON mo.id_marca = m.id_marca 
        GROUP BY m.nome_marca
    ''').fetchall()

    # 5. RETORNO PARA O TEMPLATE
    return render_template('app/dashboard.html',
                        total_veiculos=total_veiculos,
                        total_motoristas=total_motoristas,
                        perfil_completo=perfil_completo, # Envia para o HTML
                        labels_tipos=[row[0] for row in tipos_data],
                        values_tipos=[row[1] for row in tipos_data],
                        labels_marcas=[row[0] for row in marcas_data],
                        values_marcas=[row[1] for row in marcas_data],
                        username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: ADICIONAR VEÍCULO (MÁSCARA E DIGITO VERIFICADOR)
# --------------------------------------------------------------------------
@frota_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required 
def adicionar_veiculo():
    conn = get_db()
    
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        # Aqui você pode aplicar regex de placa Mercosul se desejar
        
        file = request.files.get('nf_digitalizada')
        nf_nome = None
        
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                nf_nome = secure_filename(f"NF_{placa}.{ext}")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, nf_nome))

        try:
            # Capturamos valores usando a função limpar_moeda para remover R$ e pontos
            valor_aq = limpar_moeda(request.form.get('valor_aquisicao'))
            valor_fipe = limpar_moeda(request.form.get('valor_fipe'))

            conn.execute('''
                INSERT INTO vei_imobilizado (
                    placa, renavam, chassi_veiculo, id_modelo, id_tipo, 
                    id_combustivel, km_inicial, km_atual, data_aquisicao, 
                    valor_aquisicao, valor_fipe, status_veiculo, descricao_bem
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                placa, request.form.get('renavam'), request.form.get('chassi_veiculo').upper(),
                request.form.get('id_modelo'), request.form.get('id_tipo'), 
                request.form.get('id_combustivel'), request.form.get('km_inicial', 0),
                request.form.get('km_inicial', 0), request.form.get('data_aquisicao'),
                valor_aq, valor_fipe, 'ATIVO', nf_nome
            ))
            conn.commit()
            flash(f'🚚 Veículo {placa} cadastrado com sucesso!', 'success')
            return redirect(url_for('frota.lista_frota'))
        except Exception as e:
            logging.error(f"Erro ao cadastrar veículo: {e}")
            flash(f'❌ Erro técnico: {e}', 'danger')

    # ... (restante das consultas de modelos, tipos e combustíveis permanece igual)
    modelos = conn.execute('SELECT mo.id_modelo, mo.nome_modelo, ma.nome_marca FROM vei_modelo mo JOIN vei_marca ma ON mo.id_marca = ma.id_marca ORDER BY ma.nome_marca, mo.nome_modelo').fetchall()
    tipos = conn.execute('SELECT id_tipo, nome_tipo FROM vei_tipo_carroceria ORDER BY nome_tipo').fetchall()
    combustiveis = conn.execute('SELECT id_tipo_combustivel, nome_combustivel FROM vei_combustivel ORDER BY nome_combustivel').fetchall()
    
    return render_template('app/frota/frota_adicionar.html', modelos=modelos, tipos=tipos, combustiveis=combustiveis, username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: CALCULAR VIDA ÚTIL DO PNEU (COM BASE EM 
def calcular_vida_util_pneu(id_veiculo, posicao):
    db = get_db()
    # Pega as duas últimas medições daquela posição específica
    medicoes = db.execute('''
        SELECT sulco_lido, km_veiculo_no_dia, data_medicao 
        FROM vei_pneu_medicoes 
        WHERE id_veiculo = ? AND posicao_veiculo = ?
        ORDER BY data_medicao DESC LIMIT 2
    ''', (id_veiculo, posicao)).fetchall()

    if len(medicoes) < 2:
        return "Dados insuficientes"

    m1, m2 = medicoes[0], medicoes[1] # m1 é a mais recente
    
    # 1. Cálculo de performance: KM rodada vs Desgaste em MM
    km_rodada = m1['km_veiculo_no_dia'] - m2['km_veiculo_no_dia']
    desgaste_mm = m2['sulco_lido'] - m1['sulco_lido']
    
    if desgaste_mm <= 0: return "Sem desgaste"

    # 2. Projeção: KM por milímetro
    km_por_mm = km_rodada / desgaste_mm
    
    # 3. Margem de Segurança: Consideramos borracha útil até 3mm (limite de segurança)
    borracha_util = m1['sulco_lido'] - 3.0
    km_restante = borracha_util * km_por_mm
    
    # 4. Estimativa de tempo baseada na média diária (ex: 300km/dia)
    dias_restantes = int(km_restante / 300)
    
    return f"{dias_restantes} dias"