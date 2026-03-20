# rotas/auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database import get_db
from extensions import bcrypt 
import logging

# Criação do Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

# --------------------------------------------------------------------------
# ROTA: LOGIN (Acesso de Usuários)
# --------------------------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('senha')

    if not email or not password:
        flash('Por favor, preencha todos os campos.', 'warning')
        return render_template('login.html')

    db = get_db()
    user = db.execute('SELECT id, nome, email, senha FROM login_usuarios WHERE email = ?', (email,)).fetchone()
    db.close()

    if user and bcrypt.check_password_hash(user['senha'], password):
        session['username'] = user['nome']
        session['user_id'] = user['id']
        flash(f'Bem-vindo(a), {user["nome"]}!', 'success')
        # Tenta redirecionar pelo nome da rota, se falhar, vai pelo caminho fixo
        try:
            return redirect(url_for('frota.dashboard'))
        except:
            return redirect('/frota/')
    
    flash('E-mail ou senha inválidos.', 'danger')
    return render_template('login.html')

# --------------------------------------------------------------------------
# ROTA: REGISTER (Registro de Novos Usuários)
# --------------------------------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('nome')
    email = request.form.get('email')
    password = request.form.get('senha')

    if not name or not email or not password:
        flash('Preencha todos os campos obrigatórios.', 'warning')
        return render_template('login.html')

    db = get_db()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        db.execute(
            'INSERT INTO login_usuarios (nome, email, senha) VALUES (?,?,?)',
            (name, email, hashed_password)
        )
        db.commit()
        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        logging.error(f"Erro no registro: {e}")
        flash('Erro ao cadastrar conta.', 'danger')
        return render_template('login.html')
    finally:
        db.close()

# --------------------------------------------------------------------------
# ROTA: ACESSO DIRETO (BOTÃO PARA PULAR TUDO)
# --------------------------------------------------------------------------
#@auth_bp.route('/acesso-direto')
#def acesso_direto():
#    session.clear()
#    session['user_id'] = 999
#    session['username'] = 'Israel (Dev)'
#    session['id_empresa'] = 1
#    
    # Tente estas opções na ordem se a primeira falhar:
    # Opção A: Caminho padrão do Blueprint registrado
#    return redirect('/frota')

@auth_bp.route('/acesso-direto')
def acesso_direto():
    # Simula um login automático para o desenvolvedor
    session['user_id'] = 1
    session['username'] = 'Desenvolvedor'
    # Redireciona direto para o Dashboard da Frota
    return redirect(url_for('frota.dashboard'))

# --------------------------------------------------------------------------
# ROTA: LOGOUT
# --------------------------------------------------------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('site_bp.index'))