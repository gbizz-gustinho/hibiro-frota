# rotas/site.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from database import get_db  # Necessário se processar_cadastro_teste for para o DB real
from extensions import bcrypt  # Necessário se processar_cadastro_teste for para o DB real
import logging
from flask_mail import Message # Importar Message para criar o objeto da mensagem de email

# O Blueprint é definido com 'template_folder' apontando para 'templates/site'.
# Isso significa que, dentro das rotas deste Blueprint, você pode chamar
# render_template('nome_do_arquivo.html') sem precisar do prefixo 'site/'.
site_bp = Blueprint('site_bp', __name__, template_folder='../templates/site')

# --------------------------------------------------------------------------
# ROTAS PÚBLICAS DO SITE
# --------------------------------------------------------------------------

@site_bp.route('/')
def index():
    return render_template('index.html', username=session.get('username'))

@site_bp.route('/funcionalidades')
def funcionalidades():
    return render_template('funcionalidades.html', username=session.get('username'))

@site_bp.route('/beneficios')
def beneficios():
    return render_template('beneficios.html', username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA DE CONTATO (RECEBE E PROCESSA MENSAGENS)
# --------------------------------------------------------------------------

@site_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')

        # Validação básica dos campos
        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos do formulário de contato.', 'danger')
            return render_template('contato.html', username=session.get('username'))

        # Lógica de ENVIO DE E-MAIL
        try:
            # Cria o objeto Message com os detalhes do e-mail
            msg = Message(
                subject="Nova Mensagem de Contato Hibiro 2026",
                recipients=[current_app.config['MAIL_DEFAULT_SENDER']], # Para quem o e-mail será enviado
                sender=current_app.config['MAIL_DEFAULT_SENDER'] # O remetente do e-mail
            )
            msg.body = f"""
            Você recebeu uma nova mensagem do site Hibiro 2026:

            Nome: {nome}
            E-mail: {email}
            Mensagem:
            {mensagem}
            """
            # Envia o e-mail usando a instância do Flask-Mail acessada via current_app
            current_app.extensions['mail'].send(msg)

            logging.info(f"E-mail de contato enviado com sucesso de {email}")
            flash('Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('site_bp.contato')) # Redireciona para a mesma página

        except Exception as e:
            # Loga o erro completo para depuração
            logging.error(f"ERRO ao enviar e-mail de contato de {email}: {e}", exc_info=True)
            flash('Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente mais tarde.', 'danger')
            return render_template('contato.html', username=session.get('username'))
    
    # Se a requisição for GET, apenas exibe a página de contato
    return render_template('contato.html', username=session.get('username'))

# --------------------------------------------------------------------------
# ROTAS DE CADASTRO DE TESTE GRÁTIS
# --------------------------------------------------------------------------

@site_bp.route('/cadastro-teste-gratis', methods=['GET'])
def cadastro_teste_gratis():
    """Exibe o formulário de cadastro de teste grátis."""
    return render_template('cadastro_teste_gratis.html')

@site_bp.route('/processar-cadastro-teste', methods=['POST'])
def processar_cadastro_teste():
    """Processa o envio do formulário de cadastro de teste grátis."""
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cnpj = request.form.get('cnpj', '') # Assumindo que pode ter CNPJ

    if not nome or not email or not senha:
        flash('Todos os campos (Nome, E-mail, Senha) são obrigatórios!', 'danger')
        return redirect(url_for('site_bp.cadastro_teste_gratis'))

    db = get_db()
    
    # 1. Verificar se o e-mail já existe no banco de dados REAL
    if db.execute('SELECT id FROM login_usuarios WHERE email = ?', (email,)).fetchone():
        flash('Este e-mail já está cadastrado. Tente fazer login.', 'danger')
        db.close()
        return redirect(url_for('site_bp.cadastro_teste_gratis'))

    # 2. Criar o novo usuário no banco de dados REAL
    try:
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')
        db.execute(
            'INSERT INTO login_usuarios (nome, email, senha, cnpj) VALUES (?,?,?,?)',
            (nome, email, hashed_password, cnpj)
        )
        db.commit()
        logging.info(f"Usuário {email} cadastrado com sucesso via Teste Grátis.")
        flash(f'Olá, {nome}! Sua conta foi criada com sucesso! Faça login para começar.', 'success')
        return redirect(url_for('auth.login')) # Redireciona para o login real
    except Exception as e:
        logging.error(f"Erro ao cadastrar usuário {email} via Teste Grátis: {e}", exc_info=True)
        flash(f'Ocorreu um erro ao criar sua conta. Tente novamente. ({e})', 'danger')
        return redirect(url_for('site_bp.cadastro_teste_gratis'))
    finally:
        db.close()
