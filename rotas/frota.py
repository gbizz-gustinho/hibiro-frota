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

frota_bp = Blueprint('frota', __name__, url_prefix='/frota', template_folder='../templates/app')

# --------------------------------------------------------------------------
# ROTA: DASHBOARD
# --------------------------------------------------------------------------
@frota_bp.route('/')
@login_required 
def dashboard():
    conn = get_db()
    
    # 1. CONTAR MOTORISTAS (Usa cad_clifor_colab e aux_tipoclifor)
    try:
        total_motoristas = conn.execute("""
            SELECT COUNT(*) FROM cad_clifor_colab 
            WHERE id_clifor = (SELECT Id_clifor FROM aux_tipoclifor WHERE tipo_clifor = 'MOTORISTA')
        """).fetchone()[0]
    except Exception as e:
        print(f"Erro SQL Motoristas: {e}")
        total_motoristas = 0

    # 2. TOTAL DE VEÍCULOS (Usa vei_imobilizado)
    try:
        total_veiculos = conn.execute("SELECT COUNT(*) FROM vei_imobilizado").fetchone()[0]
    except Exception as e:
        print(f"Erro SQL Veículos: {e}")
        total_veiculos = 0
    
    # 3. CONSOLIDAÇÃO DO RESUMO (Para os cards do topo)
    resumo = {
        'total_veiculos': total_veiculos,
        'total_motoristas': total_motoristas,
        'total_litros': 0.0, 
        'alertas': 5, 
        'saldo': 0.0 
    }

    # 4. DADOS PARA OS GRÁFICOS (Tipos de Veículo)
    try:
        tipos_data = conn.execute("""
            SELECT tipo_veiculo, COUNT(id_veiculo) 
            FROM vei_imobilizado 
            GROUP BY tipo_veiculo
        """).fetchall()
    except:
        tipos_data = []

    # 5. DADOS PARA OS GRÁFICOS (Marcas/Modelos)
    try:
        marcas_data = conn.execute("""
            SELECT modelo_marca, COUNT(id_veiculo) 
            FROM vei_imobilizado 
            GROUP BY modelo_marca
        """).fetchall()
    except:
        marcas_data = []

    # 6. BUSCA DOS ÚLTIMOS 5 FRETES (Tabela de Atividades)
    try:
        ultimos_fretes_db = conn.execute('''
            SELECT 
                op.id_mov_op, 
                op.data_emissao, 
                v.placa, 
                op.valor_bruto, 
                op.frete_info, 
                op.status_op
            FROM mov_operacional op
            JOIN vei_imobilizado v ON op.id_veiculo = v.id_veiculo
            ORDER BY op.data_emissao DESC 
            LIMIT 5
        ''').fetchall()
    except Exception as e:
        print(f"Erro SQL Fretes: {e}")
        ultimos_fretes_db = []

    # 7. RETORNO COMPLETO PARA O HTML
    # Não cortamos nenhuma variável aqui para o dashboard.html não dar erro de "undefined"
    return render_template('dashboard.html',
                           resumo=resumo,
                           total_veiculos=total_veiculos,
                           total_motoristas=total_motoristas,
                           labels_tipos=[row[0] for row in tipos_data],
                           values_tipos=[row[1] for row in tipos_data],
                           labels_marcas=[row[0] for row in marcas_data],
                           values_marcas=[row[1] for row in marcas_data],
                           ultimos_fretes=ultimos_fretes_db,
                           username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: LISTA DE FROTA
# --------------------------------------------------------------------------
@frota_bp.route('/lista')
@login_required 
def lista_frota():
    conn = get_db()
    veiculos_db = conn.execute('SELECT * FROM veiculos_imob ORDER BY placa').fetchall()

    veiculos_processados = []
    hoje = date.today()

    for v in veiculos_db:
        v_dict = dict(v)
        v_dict['valor_contabil_atual'] = v_dict.get('km_inicial', 0) # Exemplo usando sua estrutura
        veiculos_processados.append(v_dict)

    return render_template('frota_lista.html', 
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
        # Ajustado para os campos da sua tabela veiculos_imob
        modelo_marca = request.form.get('modelo_marca')
        tipo_veiculo = request.form.get('tipo_veiculo')
        cor = request.form.get('cor')

        try:
            conn.execute('''
                INSERT INTO veiculos_imob (placa, modelo_marca, tipo_veiculo, cor) 
                VALUES (?, ?, ?, ?)
            ''', (placa, modelo_marca, tipo_veiculo, cor))
            conn.commit()
            flash('🚚 Veículo adicionado!', 'success')
            return redirect(url_for('frota.lista_frota'))
        except Exception as e:
            flash(f'❌ Erro ao salvar: {e}', 'danger')

    return render_template('frota_adicionar.html', username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: LANÇAR FRETE
# --------------------------------------------------------------------------
@frota_bp.route('/lancar-frete', methods=['GET', 'POST'])
@login_required
def lancar_frete():
    conn = get_db()
    
    if request.method == 'POST':
        id_veiculo = request.form.get('id_veiculo')
        id_colaborador = request.form.get('id_colaborador')
        data_emissao = request.form.get('data_emissao')
        valor_bruto = request.form.get('valor_bruto').replace(',', '.')
        frete_info = f"Origem: {request.form.get('origem')} | Destino: {request.form.get('destino')}"
        id_condicao = request.form.get('id_condicao')

        try:
            cursor = conn.execute('''
                INSERT INTO mov_operacional (
                    data_emissao, id_veiculo, id_colaborador, 
                    valor_bruto, frete_info, id_condicao, status_op
                ) VALUES (?, ?, ?, ?, ?, ?, 'Concluido')
            ''', (data_emissao, id_veiculo, id_colaborador, float(valor_bruto), frete_info, id_condicao))
            
            id_mov_op = cursor.lastrowid

            conn.execute('''
                INSERT INTO mov_financeiro (
                    id_mov_op, data_vencimento, id_colaborador, 
                    valor_previsto, valor_pago
                ) VALUES (?, ?, ?, ?, 0)
            ''', (id_mov_op, data_emissao, id_colaborador, float(valor_bruto)))
            
            conn.commit()
            flash('✅ Operação de frete registrada com sucesso!', 'success')
            return redirect(url_for('frota.dashboard'))
        except Exception as e:
            conn.rollback()
            flash(f'❌ Erro ao processar: {e}', 'danger')

    veiculos = conn.execute("SELECT id_veiculo, placa, modelo_marca FROM veiculos_imob").fetchall()
    colaboradores = conn.execute("SELECT id_colaborador, nome_colaborador FROM cad_colaboradores").fetchall()
    condicoes = conn.execute("SELECT id_condicao, nome_condicao FROM aux_condicao").fetchall()
    
    return render_template('frota_lancar_frete.html', 
                           veiculos=veiculos, 
                           colaboradores=colaboradores, 
                           condicoes=condicoes,
                           date_today=date.today().isoformat())

# --------------------------------------------------------------------------
# ROTA: ADICIONAR E OU CADASTRAR COLABORADORES
# --------------------------------------------------------------------------
@frota_bp.route('/colaboradores')
@login_required
def lista_colaboradores():
    conn = get_db()
    
    # SQL usando o nome CORRETO da sua tabela
    query = '''
        SELECT 
            c.id_colaborador, 
            c.nome_colaborador, 
            c.cpf_cnpj, 
            c.municipio,
            t.tipo_clifor, 
            e.sigla
        FROM cad_clifor_colab c
        LEFT JOIN aux_tipoclifor t ON c.id_clifor = t.Id_clifor
        LEFT JOIN aux_estado e ON c.id_unifed = e.id_unifed
        ORDER BY c.nome_colaborador ASC
    '''
    
    try:
        colaboradores_db = conn.execute(query).fetchall()
    except Exception as e:
        # Se ainda der erro, o Flask vai te avisar exatamente o que é
        flash(f"Erro no banco: {e}", "danger")
        colaboradores_db = []
    
    return render_template('colaborador_lista.html', colaboradores=colaboradores_db)

@frota_bp.route('/colaboradores/novo', methods=['GET', 'POST'])
@login_required
def adicionar_colaborador():
    conn = get_db()
    
    if request.method == 'POST':
        # "Pescando" os dados do HTML usando os nomes da tabela
        nome_colaborador = request.form.get('nome_colaborador')
        cpf_cnpj = request.form.get('cpf_cnpj')
        id_pessoa = request.form.get('id_pessoa')
        id_clifor = request.form.get('id_clifor')
        id_unifed = request.form.get('id_unifed')
        municipio = request.form.get('municipio')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        try:
            conn.execute('''
                INSERT INTO cad_clifor_colab (
                    nome_colaborador, cpf_cnpj, id_pessoa, id_clifor, 
                    id_unifed, municipio, telefone, email
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome_colaborador, cpf_cnpj, id_pessoa, id_clifor, 
                  id_unifed, municipio, telefone, email))
            
            conn.commit()
            flash('✅ Colaborador cadastrado com sucesso!', 'success')
            return redirect(url_for('frota.lista_colaboradores'))
        except Exception as e:
            conn.rollback()
            flash(f'❌ Erro ao salvar na cad_clifor_colab: {e}', 'danger')

    # Busca dados para os menus de seleção (Dropdowns)
    tipos_pessoa = conn.execute("SELECT id_pessoa, tipo_pessoa FROM aux_tipopessoa").fetchall()
    tipos_clifor = conn.execute("SELECT Id_clifor, tipo_clifor FROM aux_tipoclifor").fetchall()
    estados = conn.execute("SELECT id_unifed, sigla FROM aux_estado").fetchall()

    return render_template('colaborador_adicionar.html', 
                           tipos_pessoa=tipos_pessoa, 
                           tipos_clifor=tipos_clifor, 
                           estados=estados)