from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from functools import wraps

# Definição do Blueprint
config_frota_bp = Blueprint('config_frota', __name__, url_prefix='/configuracoes/frota')

# --- DECORATOR DE SEGURANÇA ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ⛽ COMBUSTÍVEL ---
@config_frota_bp.route('/combustivel', methods=['GET', 'POST'])
@login_required
def combustivel():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_combustivel').strip().upper()
        if nome:
            db.execute('INSERT INTO vei_combustivel (nome_combustivel) VALUES (?)', (nome,))
            db.commit()
            flash(f'Combustível {nome} adicionado!', 'success')
            
    dados = db.execute('SELECT * FROM vei_combustivel ORDER BY nome_combustivel').fetchall()
    return render_template('app/frota/config_combustivel.html', combustiveis=dados, username=session.get('username'))

@config_frota_bp.route('/combustivel/editar/<int:id>', methods=['POST'])
@login_required
def editar_combustivel(id):
    db = get_db()
    novo_nome = request.form.get('nome_combustivel').strip().upper()
    if novo_nome:
        db.execute('UPDATE vei_combustivel SET nome_combustivel = ? WHERE id_tipo_combustivel = ?', (novo_nome, id))
        db.commit()
        flash('Combustível atualizado!', 'success')
    return redirect(url_for('config_frota.combustivel'))

@config_frota_bp.route('/combustivel/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_combustivel(id):
    db = get_db()
    db.execute('DELETE FROM vei_combustivel WHERE id_tipo_combustivel = ?', (id,))
    db.commit()
    flash('Combustível removido!', 'warning')
    return redirect(url_for('config_frota.combustivel'))

# --- 🏷️ MARCAS DE VEÍCULO ---
@config_frota_bp.route('/marcas', methods=['GET', 'POST'])
@login_required
def marcas():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_marca').strip().upper()
        if nome:
            db.execute('INSERT INTO vei_marca (nome_marca) VALUES (?)', (nome,))
            db.commit()
            flash(f'Marca {nome} cadastrada!', 'success')
    
    marcas_db = db.execute('SELECT * FROM vei_marca ORDER BY nome_marca').fetchall()
    return render_template('app/frota/config_marcas.html', marcas=marcas_db, username=session.get('username'))

@config_frota_bp.route('/marcas/editar/<int:id>', methods=['POST'])
@login_required
def editar_marca(id):
    db = get_db()
    novo_nome = request.form.get('nome_marca').strip().upper()
    if novo_nome:
        db.execute('UPDATE vei_marca SET nome_marca = ? WHERE id_marca = ?', (novo_nome, id))
        db.commit()
        flash('Marca atualizada!', 'success')
    return redirect(url_for('config_frota.marcas'))

@config_frota_bp.route('/marcas/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_marca(id):
    db = get_db()
    db.execute('DELETE FROM vei_marca WHERE id_marca = ?', (id,))
    db.commit()
    flash('Marca removida!', 'warning')
    return redirect(url_for('config_frota.marcas'))

# --- 🚛 MODELOS ---
@config_frota_bp.route('/modelos', methods=['GET', 'POST'])
@login_required
def modelos():
    db = get_db()
    if request.method == 'POST':
        id_marca = request.form.get('id_marca')
        nome_modelo = request.form.get('nome_modelo').strip().upper()
        if id_marca and nome_modelo:
            db.execute('INSERT INTO vei_modelo (nome_modelo, id_marca) VALUES (?,?)', (nome_modelo, id_marca))
            db.commit()
            flash(f'Modelo {nome_modelo} cadastrado!', 'success')

    modelos_db = db.execute('''
        SELECT mo.*, ma.nome_marca 
        FROM vei_modelo mo 
        JOIN vei_marca ma ON mo.id_marca = ma.id_marca 
        ORDER BY ma.nome_marca, mo.nome_modelo
    ''').fetchall()
    marcas_db = db.execute('SELECT * FROM vei_marca ORDER BY nome_marca').fetchall()
    
    return render_template('app/frota/config_modelos.html', modelos=modelos_db, marcas=marcas_db, username=session.get('username'))

@config_frota_bp.route('/modelos/editar/<int:id>', methods=['POST'])
@login_required
def editar_modelo(id):
    db = get_db()
    novo_nome = request.form.get('nome_modelo').strip().upper()
    nova_marca = request.form.get('id_marca')
    if novo_nome and nova_marca:
        db.execute('UPDATE vei_modelo SET nome_modelo = ?, id_marca = ? WHERE id_modelo = ?', (novo_nome, nova_marca, id))
        db.commit()
        flash('Modelo atualizado!', 'success')
    return redirect(url_for('config_frota.modelos'))

# --- 🏗️ TIPO DE CARROCERIA ---
@config_frota_bp.route('/tipos', methods=['GET', 'POST'])
@login_required
def config_tipo_veiculo():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_tipo').strip().upper()
        if nome:
            db.execute('INSERT INTO vei_tipo_carroceria (nome_tipo) VALUES (?)', (nome,))
            db.commit()
            flash(f'Tipo {nome} cadastrado!', 'success')
    
    tipos_db = db.execute('SELECT * FROM vei_tipo_carroceria ORDER BY nome_tipo').fetchall()
    return render_template('app/frota/config_tipo_veiculo.html', tipos=tipos_db, username=session.get('username'))

@config_frota_bp.route('/tipos/editar/<int:id>', methods=['POST'])
@login_required
def editar_tipo_veiculo(id):
    db = get_db()
    novo_nome = request.form.get('nome_tipo').strip().upper()
    if novo_nome:
        db.execute('UPDATE vei_tipo_carroceria SET nome_tipo = ? WHERE id_tipo = ?', (novo_nome, id))
        db.commit()
        flash('Tipo atualizado!', 'success')
    return redirect(url_for('config_frota.config_tipo_veiculo'))

# --- 🍩 PNEUS: MARCAS ---
@config_frota_bp.route('/pneu/marca', methods=['GET', 'POST'])
@login_required
def pneu_marca():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_marca_pneu').strip().upper()
        if nome:
            # 1. Tenta inserir
            db.execute('INSERT INTO vei_pneu_marca (nome_marca_pneu) VALUES (?)', (nome,))
            # 2. SE SALVOU, DÁ O COMMIT (IMPORTANTE!)
            db.commit()
            flash(f'Marca {nome} adicionada!', 'success')
            # 3. SE SALVOU, REDIRECIONA (ISSO ATUALIZA A TELA)
            return redirect(url_for('config_frota.pneu_marca'))
    
    # Busca a lista atualizada para mostrar na tabela
    marcas = db.execute('SELECT * FROM vei_pneu_marca ORDER BY nome_marca_pneu').fetchall()
    return render_template('app/frota/config_pneu_marca.html', marcas=marcas, username=session.get('username'))

@config_frota_bp.route('/pneu/marca/editar/<int:id>', methods=['POST'])
@login_required
def editar_pneu_marca(id):
    db = get_db()
    novo_nome = request.form.get('nome_marca_pneu').strip().upper()
    if novo_nome:
        db.execute('UPDATE vei_pneu_marca SET nome_marca_pneu = ? WHERE id_marca_pneu = ?', (novo_nome, id))
        db.commit()
        flash('Marca de pneu atualizada!', 'success')
    return redirect(url_for('config_frota.pneu_marca'))

@config_frota_bp.route('/pneu/marca/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_pneu_marca(id):
    db = get_db()
    db.execute('DELETE FROM vei_pneu_marca WHERE id_marca_pneu = ?', (id,))
    db.commit()
    flash('Marca de pneu removida!', 'warning')
    return redirect(url_for('config_frota.pneu_marca'))

# --- SITUAÇÃO DE PNEU (Novo, Recapado, etc) ---
@config_frota_bp.route('/pneu/situacao', methods=['GET', 'POST'])
@login_required
def pneu_situacao():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_situacao').strip().upper()
        if nome:
            # CORRIGIDO: Nome da tabela com prefixo vei_
            db.execute('INSERT INTO vei_pneu_situacao (nome_situacao) VALUES (?)', (nome,))
            db.commit()
            flash(f'Situação {nome} adicionada!', 'success')
            return redirect(url_for('config_frota.pneu_situacao'))
    
    # CORRIGIDO: Busca da tabela correta
    dados = db.execute('SELECT * FROM vei_pneu_situacao ORDER BY nome_situacao').fetchall()
    return render_template('app/frota/config_pneu_situacao.html', situacoes=dados, username=session.get('username'))

# --- STATUS DO VEÍCULO (Ativo, Manutenção, Venda) ---
@config_frota_bp.route('/veiculo/status', methods=['GET', 'POST'])
@login_required
def veiculo_status():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_status').strip().upper()
        if nome:
            # Verifique se no seu DB é 'vei_status' ou 'vei_veiculo_status'
            db.execute('INSERT INTO vei_status (nome_status) VALUES (?)', (nome,))
            db.commit()
            flash(f'Status {nome} adicionado!', 'success')
            return redirect(url_for('config_frota.veiculo_status'))
            
    dados = db.execute('SELECT * FROM vei_status ORDER BY nome_status').fetchall()
    return render_template('app/frota/config_veiculo_status.html', status_list=dados, username=session.get('username'))