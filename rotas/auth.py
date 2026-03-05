from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from extensions import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('frota.dashboard'))
    flash('E-mail ou senha inválidos.', 'danger')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('nome'); email = request.form.get('email')
    password = request.form.get('senha'); cnpj = request.form.get('cnpj', '')
    db = get_db()
    if db.execute('SELECT id FROM login_usuarios WHERE email = ?', (email,)).fetchone():
        flash('E-mail já cadastrado.', 'warning'); db.close()
        return redirect(url_for('auth.login'))
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    db.execute('INSERT INTO login_usuarios (nome, email, senha, cnpj) VALUES (?,?,?,?)', (name, email, hashed, cnpj))
    db.commit(); db.close()
    flash('Cadastro realizado!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear(); return redirect(url_for('site.index'))