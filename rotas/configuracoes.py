from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db

config_bp = Blueprint('configuracoes', __name__, url_prefix='/configuracoes')

# Funções Auxiliares de Verificação
def login_required():
    return session.get('username') is not None

# ==========================================
# 🤝 GESTÃO DE PARCEIROS (cad_clifor)
# ==========================================
# No cadastro de Parceiros, verifique se o HTML usa 'nome_clifor' ou 'nome_colaborador'
@config_bp.route('/parceiros', methods=['GET', 'POST'])
def config_parceiros():
    if not login_required(): return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        # Sincronizado com a coluna 'nome_colaborador' do seu SQL
        nome = request.form.get('nome_clifor').strip().upper() 
        tipo = request.form.get('tipo_clifor')
        cpf = request.form.get('cpf_cnpj')
        db.execute('INSERT INTO cad_clifor (nome_colaborador, tipo_clifor, cpf_cnpj) VALUES (?,?,?)', (nome, tipo, cpf))
        db.commit()
        flash('Parceiro adicionado com sucesso!', 'success')
    
    parceiros = db.execute('SELECT * FROM cad_clifor ORDER BY nome_colaborador').fetchall()
    return render_template('config_parceiros.html', parceiros=parceiros, username=session.get('username'))

@config_bp.route('/parceiros/editar/<int:id_colaborador>', methods=['GET', 'POST'])
def editar_parceiro(id_colaborador):
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_colaborador').strip().upper()
        tipo = request.form.get('tipo_clifor')
        db.execute('UPDATE cad_clifor SET nome_colaborador=?, tipo_clifor=? WHERE id_colaborador=?', (nome, tipo, id_colaborador))
        db.commit()
        flash('Dados atualizados!', 'success')
        return redirect(url_for('configuracoes.config_parceiros'))
    
    parceiro = db.execute('SELECT * FROM cad_clifor WHERE id_colaborador=?', (id_colaborador,)).fetchone()
    return render_template('app/config_parceiros_edit.html', parceiro=parceiro, username=session.get('username'))

@config_bp.route('/parceiros/excluir/<int:id_colaborador>', methods=['POST'])
def excluir_parceiro(id_colaborador):
    db = get_db()
    db.execute('DELETE FROM cad_clifor WHERE id_colaborador=?', (id_colaborador,))
    db.commit()
    flash('Parceiro removido!', 'warning')
    return redirect(url_for('configuracoes.config_parceiros'))

# ==========================================
# 🏷️ MARCAS E MODELOS (vei_marca / vei_modelo)
# ==========================================
@config_bp.route('/marcas', methods=['GET', 'POST'])
def config_marcas_veiculo():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_marca').strip().upper()
        db.execute('INSERT INTO vei_marca (nome_marca) VALUES (?)', (nome,))
        db.commit()
        flash('Marca cadastrada!', 'success')
    
    marcas = db.execute('SELECT * FROM vei_marca ORDER BY nome_marca').fetchall()
    return render_template('app/config_marcas.html', marcas=marcas, username=session.get('username'))

@config_bp.route('/modelos', methods=['GET', 'POST'])
def config_modelos_veiculo():
    db = get_db()
    if request.method == 'POST':
        id_marca = request.form.get('id_marca')
        nome = request.form.get('nome_modelo').strip().upper()
        db.execute('INSERT INTO vei_modelo (nome_modelo, id_marca) VALUES (?,?)', (nome, id_marca))
        db.commit()
    
    marcas = db.execute('SELECT * FROM vei_marca ORDER BY nome_marca').fetchall()
    modelos = db.execute('SELECT m.*, ma.nome_marca FROM vei_modelo m JOIN vei_marca ma ON m.id_marca = ma.id_marca').fetchall()
    return render_template('app/config_modelos.html', marcas=marcas, modelos=modelos, username=session.get('username'))

# ==========================================
# ⛽ COMBUSTÍVEIS (vei_combustivel)
# ==========================================
@config_bp.route('/combustivel', methods=['GET', 'POST'])
def config_combustivel():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_combustivel').strip().upper()
        db.execute('INSERT INTO vei_combustivel (nome_combustivel) VALUES (?)', (nome,))
        db.commit()
    
    combustiveis = db.execute('SELECT * FROM vei_combustivel').fetchall()
    return render_template('app/config_combustivel.html', combustiveis=combustiveis, username=session.get('username'))

@config_bp.route('/combustivel/editar/<int:id_tipo_combustivel>', methods=['GET', 'POST'])
def editar_combustivel(id_tipo_combustivel):
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_combustivel').strip().upper()
        db.execute('UPDATE vei_combustivel SET nome_combustivel=? WHERE id_tipo_combustivel=?', (nome, id_tipo_combustivel))
        db.commit()
        return redirect(url_for('configuracoes.config_combustivel'))
    
    c = db.execute('SELECT * FROM vei_combustivel WHERE id_tipo_combustivel=?', (id_tipo_combustivel,)).fetchone()
    return render_template('app/config_combustivel_edit.html', combustivel=c, username=session.get('username'))

# ==========================================
# 🚛 TIPOS DE VEÍCULO (vei_tipo)
# ==========================================
@config_bp.route('/tipo_veiculo', methods=['GET', 'POST'])
def config_tipo_veiculo():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_tipo').strip().upper()
        db.execute('INSERT INTO vei_tipo (nome_tipo) VALUES (?)', (nome,))
        db.commit()
    
    tipos = db.execute('SELECT * FROM vei_tipo').fetchall()
    return render_template('app/config_tipo_veiculo.html', tipos=tipos, username=session.get('username'))

@config_bp.route('/tipo_veiculo/editar/<int:id_tipo>', methods=['GET', 'POST'])
def editar_tipo_veiculo(id_tipo):
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_tipo').strip().upper()
        db.execute('UPDATE vei_tipo SET nome_tipo=? WHERE id_tipo=?', (nome, id_tipo))
        db.commit()
        return redirect(url_for('configuracoes.config_tipo_veiculo'))
    
    t = db.execute('SELECT * FROM vei_tipo WHERE id_tipo=?', (id_tipo,)).fetchone()
    return render_template('app/config_tipo_veiculo_edit.html', tipo=t, username=session.get('username'))

# ==========================================
# 🎡 MÓDULO PNEUS (Novas Tabelas do SQL)
# ==========================================
@config_bp.route('/pneu/marca', methods=['GET', 'POST'])
def config_marca_pneu():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_marca_pneu').strip().upper()
        db.execute('INSERT INTO pneu_marca (nome_marca_pneu) VALUES (?)', (nome,))
        db.commit()
    
    marcas = db.execute('SELECT * FROM pneu_marca').fetchall()
    return render_template('app/config_pneu_marca.html', marcas=marcas, username=session.get('username'))

# Rotas simples para evitar erros de 404 nos links do menu
@config_bp.route('/tipo_pessoa')
def config_tipo_pessoa(): return render_template('errors/construcao.html', username=session.get('username'))

@config_bp.route('/tipo_parceiro')
def config_tipo_parceiro(): return render_template('errors/construcao.html', username=session.get('username'))

# --- ROTAS DE PNEUS ---
@config_bp.route('/pneu/servico', methods=['GET', 'POST'])
def config_servico_pneu():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_servico').strip().upper()
        db.execute('INSERT INTO pneu_servico (nome_servico) VALUES (?)', (nome,))
        db.commit()
    servicos = db.execute('SELECT * FROM pneu_servico').fetchall()
    # Enquanto não cria o HTML específico, usamos o geral ou um aviso
    return render_template('app/config_pneu_servico.html', servicos=servicos, username=session.get('username'))

@config_bp.route('/pneu/situacao', methods=['GET', 'POST'])
def config_situacao_pneu():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_situacao').strip().upper()
        db.execute('INSERT INTO pneu_situacao (nome_situacao) VALUES (?)', (nome,))
        db.commit()
    situacoes = db.execute('SELECT * FROM pneu_situacao').fetchall()
    return render_template('app/config_pneu_situacao.html', situacoes=situacoes, username=session.get('username'))

# --- ROTAS "CURATIVO" (Para o menu não quebrar) ---
@config_bp.route('/orgao_emissor')
def config_orgao_emissor(): return "Página em construção"

@config_bp.route('/gravidade_multa')
def config_gravidade_multa(): return "Página em construção"

@config_bp.route('/status_documento')
def config_status_documento(): return "Página em construção"

@config_bp.route('/status_manutencao')
def config_status_manutencao(): return "Página em construção"

@config_bp.route('/tipo_manutencao')
def config_tipo_manutencao(): return "Página em construção"

@config_bp.route('/status_frete')
def config_status_frete(): return "Página em construção"

@config_bp.route('/tipo_servico')
def config_tipo_servico(): return "Página em construção"

@config_bp.route('/status_servico')
def config_status_servico(): return "Página em construção"