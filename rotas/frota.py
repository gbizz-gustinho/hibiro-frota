# rotas/frota.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from database import get_db 
from functools import wraps
import logging

# --- DECORATOR PARA EXIGIR LOGIN ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado(a) para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- DEFINIÇÃO DO BLUEPRINT DA FROTA ---
# CORRIGIDO: 'template_folder' agora aponta DIRETAMENTE para a pasta ONDE ESTÃO SEUS TEMPLATES DE APP.
# Ou seja, 'templates/app'.
frota_bp = Blueprint('frota', __name__, url_prefix='/frota', template_folder='../templates/app')

# --------------------------------------------------------------------------
# ROTA: DASHBOARD (Página Principal da Frota)
# Acesso protegido por login_required.
# --------------------------------------------------------------------------
@frota_bp.route('/')
@login_required 
def dashboard():
    logging.info(f"Usuário '{session.get('username')}' ({session.get('user_id')}) acessou o dashboard.")
    conn = get_db()
    
    total_motoristas = conn.execute("SELECT COUNT(*) FROM cad_clifor WHERE tipo_clifor = 'MOTORISTA'").fetchone()[0]
    total_veiculos = conn.execute("SELECT COUNT(*) FROM vei_imobilizado WHERE status_veiculo = 'ATIVO'").fetchone()[0]

    tipos_data = conn.execute('''
        SELECT t.nome_tipo, COUNT(v.id_veiculo) 
        FROM vei_imobilizado v 
        JOIN vei_tipo t ON v.id_tipo = t.id_tipo 
        GROUP BY t.nome_tipo
    ''').fetchall()
    
    marcas_data = conn.execute('''
        SELECT m.nome_marca, COUNT(v.id_veiculo) 
        FROM vei_imobilizado v 
        JOIN vei_modelo mo ON v.id_modelo = mo.id_modelo 
        JOIN vei_marca m ON mo.id_marca = m.id_marca 
        GROUP BY m.nome_marca
    ''').fetchall()

    # Renderiza o template do dashboard, passando os dados e o nome do usuário da sessão.
    # Não precisa de nenhum prefixo, pois o template_folder já aponta para 'templates/app'.
    return render_template('dashboard.html',
                           total_veiculos=total_veiculos,
                           total_motoristas=total_motoristas,
                           labels_tipos=[row[0] for row in tipos_data],
                           values_tipos=[row[1] for row in tipos_data],
                           labels_marcas=[row[0] for row in marcas_data],
                           values_marcas=[row[1] for row in marcas_data],
                           username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: LISTA DE FROTA
# Exibe uma lista detalhada de veículos com cálculo de depreciação.
# Acesso protegido por login_required.
# --------------------------------------------------------------------------
@frota_bp.route('/lista')
@login_required 
def lista_frota():
    logging.info(f"Usuário '{session.get('username')}' ({session.get('user_id')}) acessou a lista de frota.")
    conn = get_db()
    
    veiculos_db = conn.execute('''
        SELECT v.id_veiculo, v.placa, v.data_aquisicao, v.valor_aquisicao, v.taxa_depreciacao_anual,
               m.nome_marca, mo.nome_modelo, t.nome_tipo
        FROM vei_imobilizado v
        JOIN vei_modelo mo ON v.id_modelo = mo.id_modelo
        JOIN vei_marca m ON mo.id_marca = m.id_marca
        JOIN vei_tipo t ON v.id_tipo = t.id_tipo
        ORDER BY v.placa
    ''').fetchall()

    veiculos_processados = []
    hoje = date.today()

    for v in veiculos_db:
        v_dict = dict(v)
        # Cálculo de Depreciação Contábil
        try:
            data_aq = date.fromisoformat(v_dict['data_aquisicao'])
            anos_uso = (hoje - data_aq).days / 365.25
            valor_original = v_dict['valor_aquisicao'] or 0
            taxa = (v_dict['taxa_depreciacao_anual'] or 20) / 100
            
            valor_contabil = valor_original - (valor_original * taxa * anos_uso)
            v_dict['valor_contabil_atual'] = max(valor_contabil, 0)
        except Exception as e:
            logging.error(f"Erro ao calcular depreciação para veículo {v_dict.get('placa')}: {e}", exc_info=True)
            v_dict['valor_contabil_atual'] = v_dict['valor_aquisicao'] or 0
            
        # Formata data para o padrão Brasil na lista
        try:
            v_dict['data_formatada'] = date.fromisoformat(v_dict['data_aquisicao']).strftime('%d/%m/%Y')
        except Exception as e:
            logging.error(f"Erro ao formatar data de aquisição para veículo {v_dict.get('placa')}: {e}", exc_info=True)
            v_dict['data_formatada'] = v_dict['data_aquisicao']

        veiculos_processados.append(v_dict)

    # Renderiza o template da lista de frota.
    return render_template('frota_lista.html', veiculos=veiculos_processados, username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: ADICIONAR VEÍCULO
# Gerencia o formulário e a lógica para adicionar novos veículos.
# Acesso protegido por login_required.
# --------------------------------------------------------------------------
@frota_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required 
def adicionar_veiculo():
    logging.info(f"Usuário '{session.get('username')}' ({session.get('user_id')}) acessou adicionar veículo.")
    conn = get_db()
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        id_modelo = request.form.get('id_modelo')
        id_tipo = request.form.get('id_tipo')
        data_aquisicao = request.form.get('data_aquisicao')
        valor_aq = request.form.get('valor_aquisicao', '0').replace(',', '.')

        try:
            conn.execute('''
                INSERT INTO vei_imobilizado (placa, id_modelo, id_tipo, data_aquisicao, valor_aquisicao, status_veiculo) 
                VALUES (?,?,?,?,?, 'ATIVO')
            ''', (placa, id_modelo, id_tipo, data_aquisicao, float(valor_aq)))
            conn.commit()
            flash('🚚 Veículo adicionado com sucesso!', 'success')
            return redirect(url_for('frota.lista_frota'))
        except Exception as e:
            logging.error(f"Erro ao adicionar veículo para usuário '{session.get('username')}': {e}", exc_info=True)
            flash(f'❌ Erro ao salvar: {e}', 'danger')

    modelos = conn.execute('SELECT id_modelo, nome_modelo FROM vei_modelo ORDER BY nome_modelo').fetchall()
    tipos = conn.execute('SELECT id_tipo, nome_tipo FROM vei_tipo ORDER BY nome_tipo').fetchall()
    # Renderiza o template de adicionar veículo.
    return render_template('frota_adicionar.html', modelos=modelos, tipos=tipos, username=session.get('username'))