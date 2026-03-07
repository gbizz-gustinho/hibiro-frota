# rotas/auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database import get_db
from extensions import bcrypt # Para fazer hash e checar senhas
import logging

# Criação do Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

# --------------------------------------------------------------------------
# ROTA: LOGIN (Acesso de Usuários)
# Exibe o formulário de login (GET) ou processa a autenticação (POST).
# --------------------------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Exibe o formulário de login (GET) ou processa a autenticação (POST)."""
    if request.method == 'GET':
        return render_template('login.html')

    # Processamento da requisição POST (tentativa de login)
    email = request.form.get('email')
    password = request.form.get('senha')

    # Validação: verifica se ambos os campos foram preenchidos
    if not email or not password:
        flash('Por favor, preencha todos os campos.', 'warning')
        return render_template('login.html')

    # Abre a conexão com o banco de dados
    db = get_db()
    # Busca o usuário pelo e-mail
    user = db.execute('SELECT id, nome, email, senha FROM login_usuarios WHERE email = ?', (email,)).fetchone()
    db.close() # Fecha a conexão com o banco de dados

    # Lógica de autenticação e feedback ao usuário
    if user: # Se o e-mail foi encontrado no banco de dados
        if bcrypt.check_password_hash(user['senha'], password): # Verifica se a senha está correta
            # Autenticação bem-sucedida: inicia a sessão do usuário
            session['username'] = user['nome']
            session['user_id'] = user['id']
            logging.info(f"Usuário '{email}' logado com sucesso.")
            flash(f'Bem-vindo(a), {user["nome"]}!', 'success')
            return redirect(url_for('frota.dashboard')) # Redireciona para o dashboard
        else:
            # Usuário encontrado, mas senha incorreta
            logging.warning(f"Tentativa de login falhou: Senha incorreta para '{email}'.")
            flash('Senha incorreta. Por favor, tente novamente.', 'danger')
            return render_template('login.html')
    else:
        # E-mail não encontrado no banco de dados
        logging.warning(f"Tentativa de login falhou: E-mail '{email}' não encontrado.")
        flash('E-mail não cadastrado. Por favor, verifique ou crie uma conta.', 'danger')
        return render_template('login.html')

# --------------------------------------------------------------------------
# ROTA: REGISTER (Registro de Novos Usuários)
# Processa o registro de um novo usuário via formulário.
# --------------------------------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    """Processa o registro de um novo usuário (usado pelo formulário de login/registro)."""
    name = request.form.get('nome')
    email = request.form.get('email')
    password = request.form.get('senha')
    cnpj = request.form.get('cnpj', '') # CNPJ pode ser opcional

    # Validação: verifica se campos obrigatórios foram preenchidos
    if not name or not email or not password:
        flash('Todos os campos obrigatórios (Nome, E-mail, Senha) devem ser preenchidos.', 'warning')
        return render_template('login.html')

    db = get_db()
    
    # Verifica se o e-mail já existe no banco de dados
    if db.execute('SELECT id FROM login_usuarios WHERE email = ?', (email,)).fetchone():
        flash('Este e-mail já está cadastrado. Por favor, tente fazer login.', 'warning')
        db.close()
        return render_template('login.html')

    # Gera o hash da senha antes de salvar no banco de dados
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        # Insere o novo usuário no banco de dados
        db.execute(
            'INSERT INTO login_usuarios (nome, email, senha, cnpj) VALUES (?,?,?,?)',
            (name, email, hashed_password, cnpj)
        )
        db.commit() # Salva as alterações no banco
        logging.info(f"Novo usuário registrado via formulário: '{email}'")
        flash('Sua conta foi criada com sucesso! Por favor, faça login.', 'success')
        return redirect(url_for('auth.login')) # Redireciona para a página de login
    except Exception as e:
        # Captura e loga quaisquer erros durante o registro
        logging.error(f"Erro ao registrar usuário '{email}': {e}", exc_info=True)
        flash(f'Ocorreu um erro ao tentar cadastrar sua conta. Detalhes: {e}', 'danger')
        return render_template('login.html')
    finally:
        db.close() # Garante que a conexão com o banco seja fechada

# --------------------------------------------------------------------------
# ROTA: LOGOUT (Finalizar Sessão)
# Desloga o usuário, limpando a sessão.
# --------------------------------------------------------------------------
@auth_bp.route('/logout')
def logout():
    """Desloga o usuário, limpando a sessão."""
    user_email = session.get('username', 'Usuário Desconhecido') # Pega o username para log
    session.clear() # Limpa todos os dados da sessão
    logging.info(f"Usuário '{user_email}' deslogado.")
    flash('Você saiu da sua conta com segurança.', 'info')
    return redirect(url_for('site_bp.index')) # Redireciona para a página inicial