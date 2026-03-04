from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template



app = Flask(__name__)
app.secret_key = 'chave_secreta_desenvolvimento_hibiro' 
bcrypt = Bcrypt(app)

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'dados', 'hibiro_frota.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# --- FILTROS PERSONALIZADOS ---
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

# --- ROTAS DO SITE (VITRINE) ---
@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template('site/index.html')

@app.route('/funcionalidades')
def funcionalidades(): return render_template('site/funcionalidades.html')

@app.route('/beneficios')
def beneficios(): return render_template('site/beneficios.html')

@app.route('/contato')
def contato(): return render_template('site/contato.html')

# --- AUTENTICAÇÃO ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET': return render_template('auth/login.html')
    email = request.form.get('email')
    password = request.form.get('senha')
    db = get_db()
    user = db.execute('SELECT * FROM login_usuarios WHERE email = ?', (email,)).fetchone()
    db.close()
    if user and bcrypt.check_password_hash(user['senha'], password):
        session['username'] = user['nome']
        session['user_id'] = user['id']
        return redirect(url_for('dashboard'))
    flash('E-mail ou senha inválidos.', 'danger')
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('nome'); email = request.form.get('email')
    password = request.form.get('senha'); cnpj = request.form.get('cnpj', '')
    db = get_db()
    if db.execute('SELECT id FROM login_usuarios WHERE email = ?', (email,)).fetchone():
        flash('E-mail já cadastrado.', 'warning'); db.close()
        return redirect(url_for('login'))
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    db.execute('INSERT INTO login_usuarios (nome, email, senha, cnpj) VALUES (?,?,?,?)', (name, email, hashed, cnpj))
    db.commit(); db.close()
    flash('Cadastro realizado!', 'success')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('index'))

# --- ÁREA LOGADA: DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    stats = {
        'motoristas': db.execute('SELECT COUNT(*) FROM clifor_motorista').fetchone()[0],
        'veiculos': db.execute('SELECT COUNT(*) FROM veiculos_imobilizado_novo').fetchone()[0],
        'marcas': db.execute('SELECT COUNT(*) FROM marca_veiculo').fetchone()[0]
    }
    db.close()
    return render_template('app/dashboard.html', username=session['username'], **stats)

# --- GESTÃO DE FROTA ---
@app.route('/frota/lista')
def lista_frota():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    veiculos_raw = db.execute('''
        SELECT v.*, m.nome_modelo, ma.nome_marca, t.nome_tipo 
        FROM veiculos_imobilizado_novo v 
        JOIN modelo_veiculo m ON v.id_modelo = m.id_modelo 
        JOIN marca_veiculo ma ON m.id_marca = ma.id_marca
        JOIN tipo_veiculo t ON v.id_tipo = t.id_tipo
    ''').fetchall()
    db.close()
    
    hoje = datetime.now()
    processados = []
    for v in veiculos_raw:
        item = dict(v)
        if v['data_aquisicao'] and v['valor_aquisicao']:
            data = datetime.strptime(v['data_aquisicao'], '%Y-%m-%d')
            anos = (hoje - data).days / 365.25
            taxa = (v['taxa_depreciacao_anual'] or 20) / 100
            atual = v['valor_aquisicao'] - (v['valor_aquisicao'] * taxa * anos)
            item['valor_contabil_atual'] = max(atual, v['valor_aquisicao'] * 0.1)
        else:
            item['valor_contabil_atual'] = v['valor_aquisicao'] or 0
        processados.append(item)
    return render_template('app/frota_lista.html', username=session['username'], veiculos=processados)

@app.route('/frota/adicionar', methods=['GET', 'POST'])
def adicionar_veiculo():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        dados = (request.form.get('placa'), request.form.get('id_modelo'), request.form.get('id_tipo'),
                 request.form.get('data_aquisicao'), request.form.get('valor_aquisicao'))
        db.execute('INSERT INTO veiculos_imobilizado_novo (placa, id_modelo, id_tipo, data_aquisicao, valor_aquisicao) VALUES (?,?,?,?,?)', dados)
        db.commit(); db.close()
        return redirect(url_for('lista_frota'))
    
    marcas = db.execute('SELECT * FROM marca_veiculo').fetchall()
    tipos = db.execute('SELECT * FROM tipo_veiculo').fetchall()
    db.close()
    return render_template('app/frota_form.html', username=session['username'], marcas=marcas, tipos=tipos)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ✨ SEÇÃO DE EDIÇÃO (NOVIDADES PARA O SEU CHECK ✅)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route('/configuracoes/marcas/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        novo_nome = request.form.get('nome_marca').upper()
        db.execute('UPDATE marca_veiculo SET nome_marca = ? WHERE id_marca = ?', (novo_nome, id))
        db.commit(); db.close()
        flash('Marca atualizada com sucesso!', 'success')
        return redirect(url_for('config_marcas'))
    marca = db.execute('SELECT * FROM marca_veiculo WHERE id_marca = ?', (id,)).fetchone()
    db.close()
    return render_template('app/config_marcas_edit.html', username=session['username'], marca=marca)

@app.route('/configuracoes/modelos/editar/<int:id>', methods=['GET', 'POST'])
def editar_modelo(id):
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        novo_nome = request.form.get('nome_modelo').upper()
        id_marca = request.form.get('id_marca')
        db.execute('UPDATE modelo_veiculo SET nome_modelo = ?, id_marca = ? WHERE id_modelo = ?', (novo_nome, id_marca, id))
        db.commit(); db.close()
        flash('Modelo atualizado!', 'success')
        return redirect(url_for('config_modelos'))
    modelo = db.execute('SELECT * FROM modelo_veiculo WHERE id_modelo = ?', (id,)).fetchone()
    marcas = db.execute('SELECT * FROM marca_veiculo').fetchall()
    db.close()
    return render_template('app/config_modelos_edit.html', username=session['username'], modelo=modelo, marcas=marcas)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# --- CONFIGURAÇÕES ORIGINAIS ---
@app.route('/configuracoes/marcas', methods=['GET', 'POST'])
def config_marcas():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO marca_veiculo (nome_marca) VALUES (?)', (request.form.get('nome_marca').upper(),))
        db.commit()
    marcas = db.execute('SELECT * FROM marca_veiculo ORDER BY nome_marca').fetchall()
    db.close(); return render_template('app/config_marcas.html', username=session['username'], marcas=marcas)

@app.route('/configuracoes/modelos', methods=['GET', 'POST'])
def config_modelos():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO modelo_veiculo (nome_modelo, id_marca) VALUES (?,?)', (request.form.get('nome_modelo').upper(), request.form.get('id_marca')))
        db.commit()
    modelos = db.execute('SELECT m.*, ma.nome_marca FROM modelo_veiculo m JOIN marca_veiculo ma ON m.id_marca = ma.id_marca').fetchall()
    marcas = db.execute('SELECT * FROM marca_veiculo').fetchall()
    db.close(); return render_template('app/config_modelos.html', username=session['username'], modelos=modelos, marcas=marcas)

@app.route('/configuracoes/combustivel', methods=['GET', 'POST'])
def config_combustivel():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO tipo_combustivel (nome_combustivel) VALUES (?)', (request.form.get('nome_combustivel').upper(),))
        db.commit()
    itens = db.execute('SELECT * FROM tipo_combustivel').fetchall()
    db.close(); return render_template('app/config_combustivel.html', username=session['username'], combustiveis=itens)

@app.route('/configuracoes/tipo-veiculo', methods=['GET', 'POST'])
def config_tipo_veiculo():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO tipo_veiculo (nome_tipo) VALUES (?)', (request.form.get('nome_tipo').upper(),))
        db.commit()
    tipos = db.execute('SELECT * FROM tipo_veiculo').fetchall()
    db.close(); return render_template('app/config_tipo_veiculo.html', username=session['username'], tipos=tipos)

@app.route('/configuracoes/parceiros', methods=['GET', 'POST'])
def config_parceiros():
    if 'username' not in session: return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO clifor_motorista (nome_colaborador, cpf_cnpj, tipo_clifor) VALUES (?,?,?)', 
                   (request.form.get('nome_colaborador').upper(), request.form.get('cpf_cnpj'), request.form.get('tipo_clifor')))
        db.commit()
    parceiros = db.execute('SELECT * FROM clifor_motorista').fetchall()
    db.close(); return render_template('app/config_parceiros.html', username=session['username'], parceiros=parceiros)

# --- ROTAS DE EXCLUSÃO ---
@app.route('/excluir_marca/<int:id>')
def excluir_marca(id):
    db = get_db(); db.execute('DELETE FROM marca_veiculo WHERE id_marca = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('config_marcas'))

@app.route('/excluir_modelo/<int:id>')
def excluir_modelo(id):
    db = get_db(); db.execute('DELETE FROM modelo_veiculo WHERE id_modelo = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('config_modelos'))

@app.route('/excluir_combustivel/<int:id>')
def excluir_combustivel(id):
    db = get_db(); db.execute('DELETE FROM tipo_combustivel WHERE id_tipo_combustivel = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('config_combustivel'))

@app.route('/excluir_tipo_veiculo/<int:id>')
def excluir_tipo_veiculo(id):
    db = get_db(); db.execute('DELETE FROM tipo_veiculo WHERE id_tipo = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('config_tipo_veiculo'))

@app.route('/excluir_parceiro/<int:id>')
def excluir_parceiro(id):
    db = get_db(); db.execute('DELETE FROM clifor_motorista WHERE id = ?', (id,)); db.commit(); db.close()
    return redirect(url_for('config_parceiros'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)