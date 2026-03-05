from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db

config_bp = Blueprint('configuracoes', __name__)

@config_bp.route('/configuracoes/marcas', methods=['GET', 'POST'])
def config_marcas():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO marca_veiculo (nome_marca) VALUES (?)', (request.form.get('nome_marca').upper(),))
        db.commit()
    marcas = db.execute('SELECT * FROM marca_veiculo ORDER BY nome_marca').fetchall()
    db.close(); return render_template('app/config_marcas.html', username=session['username'], marcas=marcas)

@config_bp.route('/configuracoes/marcas/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        novo_nome = request.form.get('nome_marca').upper()
        db.execute('UPDATE marca_veiculo SET nome_marca = ? WHERE id_marca = ?', (novo_nome, id))
        db.commit(); db.close()
        flash('Marca atualizada com sucesso!', 'success')
        return redirect(url_for('configuracoes.config_marcas'))
    marca = db.execute('SELECT * FROM marca_veiculo WHERE id_marca = ?', (id,)).fetchone()
    db.close()
    return render_template('app/config_marcas_edit.html', username=session['username'], marca=marca)

@config_bp.route('/configuracoes/modelos', methods=['GET', 'POST'])
def config_modelos():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO modelo_veiculo (nome_modelo, id_marca) VALUES (?,?)', (request.form.get('nome_modelo').upper(), request.form.get('id_marca')))
        db.commit()
    modelos = db.execute('SELECT m.*, ma.nome_marca FROM modelo_veiculo m JOIN marca_veiculo ma ON m.id_marca = ma.id_marca').fetchall()
    marcas = db.execute('SELECT * FROM marca_veiculo').fetchall()
    db.close(); return render_template('app/config_modelos.html', username=session['username'], modelos=modelos, marcas=marcas)

@config_bp.route('/configuracoes/modelos/editar/<int:id>', methods=['GET', 'POST'])
def editar_modelo(id):
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        novo_nome = request.form.get('nome_modelo').upper()
        id_marca = request.form.get('id_marca')
        db.execute('UPDATE modelo_veiculo SET nome_modelo = ?, id_marca = ? WHERE id_modelo = ?', (novo_nome, id_marca, id))
        db.commit(); db.close()
        flash('Modelo atualizado!', 'success')
        return redirect(url_for('configuracoes.config_modelos'))
    modelo = db.execute('SELECT * FROM modelo_veiculo WHERE id_modelo = ?', (id,)).fetchone()
    marcas = db.execute('SELECT * FROM marca_veiculo').fetchall()
    db.close()
    return render_template('app/config_modelos_edit.html', username=session['username'], modelo=modelo, marcas=marcas)

@config_bp.route('/configuracoes/combustivel', methods=['GET', 'POST'])
def config_combustivel():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO tipo_combustivel (nome_combustivel) VALUES (?)', (request.form.get('nome_combustivel').upper(),))
        db.commit()
    itens = db.execute('SELECT * FROM tipo_combustivel').fetchall()
    db.close(); return render_template('app/config_combustivel.html', username=session['username'], combustiveis=itens)

@config_bp.route('/configuracoes/tipo-veiculo', methods=['GET', 'POST'])
def config_tipo_veiculo():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO tipo_veiculo (nome_tipo) VALUES (?)', (request.form.get('nome_tipo').upper(),))
        db.commit()
    tipos = db.execute('SELECT * FROM tipo_veiculo').fetchall()
    db.close(); return render_template('app/config_tipo_veiculo.html', username=session['username'], tipos=tipos)

@config_bp.route('/configuracoes/parceiros', methods=['GET', 'POST'])
def config_parceiros():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO clifor_motorista (nome_colaborador, cpf_cnpj, tipo_clifor) VALUES (?,?,?)', 
                   (request.form.get('nome_colaborador').upper(), request.form.get('cpf_cnpj'), request.form.get('tipo_clifor')))
        db.commit()
    parceiros = db.execute('SELECT * FROM clifor_motorista').fetchall()
    db.close(); return render_template('app/config_parceiros.html', username=session['username'], parceiros=parceiros)

@config_bp.route('/excluir_marca/<int:id>')
def excluir_marca(id):
    db = get_db(); db.execute('DELETE FROM marca_veiculo WHERE id_marca = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('configuracoes.config_marcas'))

@config_bp.route('/excluir_modelo/<int:id>')
def excluir_modelo(id):
    db = get_db(); db.execute('DELETE FROM modelo_veiculo WHERE id_modelo = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('configuracoes.config_modelos'))

@config_bp.route('/excluir_combustivel/<int:id>')
def excluir_combustivel(id):
    db = get_db(); db.execute('DELETE FROM tipo_combustivel WHERE id_tipo_combustivel = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('configuracoes.config_combustivel'))

@config_bp.route('/excluir_tipo_veiculo/<int:id>')
def excluir_tipo_veiculo(id):
    db = get_db(); db.execute('DELETE FROM tipo_veiculo WHERE id_tipo = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('configuracoes.config_tipo_veiculo'))

@config_bp.route('/excluir_parceiro/<int:id>')
def excluir_parceiro(id):
    db = get_db(); db.execute('DELETE FROM clifor_motorista WHERE id = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('configuracoes.config_parceiros'))