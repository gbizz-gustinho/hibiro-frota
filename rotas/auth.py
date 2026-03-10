from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database import get_db
from extensions import bcrypt
import logging

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

# --------------------------------------------------------------------------
# ROTA: LOGIN (Versão única e funcional)
# --------------------------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('senha')

    if not email or not password:
        flash('Por favor, informe e-mail e senha.', 'warning')
        return render_template('login.html')

    db = get_db()
    # Busca o usuário pelo e-mail
    user = db.execute('SELECT id, nome, email, senha FROM login_usuarios WHERE email = ?', (email,)).fetchone()

    # 1. VERIFICA SE O USUÁRIO EXISTE E A SENHA ESTÁ CORRETA
    if user and bcrypt.check_password_hash(user['senha'], password):
        session.clear()
        session['username'] = user['nome']
        session['user_id'] = user['id']
        
        # 2. BUSCA O CNPJ PARA A TRAVA DO SAAS
        empresa = db.execute('SELECT CNPJ FROM cad_empresa WHERE id_usuario = ?', (user['id'],)).fetchone()
        
        # 3. LÓGICA DE REDIRECIONAMENTO
        if not empresa or empresa['CNPJ'] in ["00000000000000", "", None]:
            session['perfil_completo'] = False # Trava a sidebar
            flash(f'Olá {user["nome"]}! Complete o perfil da empresa para liberar o sistema.', 'info')
            return redirect(url_for('parceiros_bases.perfil_empresa')) 
        else:
            session['perfil_completo'] = True # Libera a sidebar
            flash(f'Bem-vindo de volta, {user["nome"]}!', 'success')
            return redirect(url_for('frota.dashboard'))

    # 4. TRATAMENTO DE ERRO (Sempre retorna algo para o Flask)
    flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')

# --------------------------------------------------------------------------
# ROTA: REGISTER (Onboarding Integral)
# --------------------------------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
@auth_bp.route('/processar-cadastro-teste', methods=['POST'])
def register():
    name = request.form.get('nome', '').strip().upper()
    email = request.form.get('email', '').strip()
    password = request.form.get('senha')

    if not name or not email or not password:
        flash('Todos os campos são obrigatórios.', 'warning')
        return redirect(url_for('site_bp.cadastro_teste_gratis'))

    db = get_db()
    if db.execute('SELECT id FROM login_usuarios WHERE email = ?', (email,)).fetchone():
        flash('Este e-mail já está cadastrado.', 'warning')
        return redirect(url_for('auth.login'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        # 1. Cria Usuário
        cursor = db.execute('INSERT INTO login_usuarios (nome, email, senha) VALUES (?,?,?)', (name, email, hashed_password))
        novo_id = cursor.lastrowid

        # 2. Cria Empresa Provisória
        db.execute('INSERT INTO cad_empresa (id_usuario, razao_social, CNPJ) VALUES (?, ?, ?)', 
                   (novo_id, f"TRANSPORTADORA DE {name}", "00000000000000"))
        db.commit()
        
        flash('Cadastro realizado! Agora você já pode entrar.', 'success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        db.rollback()
        logging.error(f"Erro no Onboarding: {e}")
        flash('Erro interno ao criar conta.', 'danger')
        return redirect(url_for('site_bp.cadastro_teste_gratis'))

# --------------------------------------------------------------------------
# ROTA: LOGOUT
# --------------------------------------------------------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('site_bp.index'))