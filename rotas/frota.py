import os
import logging
from datetime import date
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import get_db 

# Configurações de Upload
UPLOAD_FOLDER = 'static/uploads/nfs'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# --- BLUEPRINT (Simples e Direto) ---
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

# --- AUXILIAR DE MOEDA ---
def limpar_moeda(v):
    if not v: return 0.0
    return float(str(v).replace('.', '').replace(',', '.'))

# --------------------------------------------------------------------------
# ROTA: DASHBOARD
# --------------------------------------------------------------------------
@frota_bp.route('/')
@login_required 
def dashboard():
    conn = get_db()
    
    total_motoristas = conn.execute("SELECT COUNT(*) FROM cad_clifor WHERE tipo_clifor = 'MOTORISTA'").fetchone()[0]
    total_veiculos = conn.execute("SELECT COUNT(*) FROM vei_imobilizado WHERE status_veiculo = 'ATIVO'").fetchone()[0]

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

    return render_template('app/dashboard.html',
                        total_veiculos=total_veiculos,
                        total_motoristas=total_motoristas,
                        labels_tipos=[row[0] for row in tipos_data],
                        values_tipos=[row[1] for row in tipos_data],
                        labels_marcas=[row[0] for row in marcas_data],
                        values_marcas=[row[1] for row in marcas_data],
                        username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: LISTA DE FROTA
# --------------------------------------------------------------------------
@frota_bp.route('/lista')
@login_required 
def lista_frota():
    conn = get_db()
    hoje = date.today()
    
    veiculos_db = conn.execute('''
        SELECT v.id_veiculo, v.placa, v.data_aquisicao, v.valor_aquisicao, v.taxa_depreciacao_anual,
               v.valor_fipe, v.descricao_bem as nf_caminho,
               m.nome_marca, mo.nome_modelo, t.nome_tipo
        FROM vei_imobilizado v
        JOIN vei_modelo mo ON v.id_modelo = mo.id_modelo
        JOIN vei_marca m ON mo.id_marca = m.id_marca
        JOIN vei_tipo_carroceria t ON v.id_tipo = t.id_tipo
        ORDER BY v.placa
    ''').fetchall()

    veiculos_processados = []

    for v in veiculos_db:
        v_dict = dict(v)
        try:
            dt_aq = date.fromisoformat(v_dict['data_aquisicao'])
            anos_uso = (hoje - dt_aq).days / 365.25
            v_orig = v_dict['valor_aquisicao'] or 0
            taxa = (v_dict['taxa_depreciacao_anual'] or 20) / 100
            valor_depreciado = v_orig - (v_orig * taxa * anos_uso)
            v_dict['valor_contabil_atual'] = max(valor_depreciado, 0)
            v_dict['data_formatada'] = dt_aq.strftime('%d/%m/%Y')
        except:
            v_dict['valor_contabil_atual'] = v_dict['valor_aquisicao'] or 0
            v_dict['data_formatada'] = v_dict['data_aquisicao']
        veiculos_processados.append(v_dict)

    return render_template('app/frota/frota_lista.html', 
                           veiculos=veiculos_processados, 
                           username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: ADICIONAR VEÍCULO
# --------------------------------------------------------------------------
@frota_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required 
def adicionar_veiculo():
    conn = get_db()
    
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        file = request.files.get('nf_digitalizada')
        nf_nome = None
        
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                nf_nome = secure_filename(f"NF_{placa}.{ext}")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, nf_nome))

        try:
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
                limpar_moeda(request.form.get('valor_aquisicao')), 
                limpar_moeda(request.form.get('valor_fipe')), 
                'ATIVO', nf_nome
            ))
            conn.commit()
            flash(f'🚚 Veículo {placa} cadastrado com sucesso!', 'success')
            return redirect(url_for('frota.lista_frota'))
        except Exception as e:
            logging.error(f"Erro ao cadastrar: {e}")
            flash(f'❌ Erro técnico: {e}', 'danger')

    modelos = conn.execute('''
        SELECT mo.id_modelo, mo.nome_modelo, ma.nome_marca 
        FROM vei_modelo mo 
        JOIN vei_marca ma ON mo.id_marca = ma.id_marca 
        ORDER BY ma.nome_marca
    ''').fetchall()
    tipos = conn.execute('SELECT id_tipo, nome_tipo FROM vei_tipo_carroceria').fetchall()
    combustiveis = conn.execute('SELECT id_tipo_combustivel, nome_combustivel FROM vei_combustivel').fetchall()
    
    return render_template('app/frota/frota_adicionar.html', 
                           modelos=modelos, 
                           tipos=tipos, 
                           combustiveis=combustiveis, 
                           username=session.get('username'))