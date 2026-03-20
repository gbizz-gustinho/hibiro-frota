# rotas/site.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from database import get_db 
from extensions import bcrypt 
import logging
from flask_mail import Message

site_bp = Blueprint('site_bp', __name__, template_folder='../templates/site')

# --- ROTAS PÚBLICAS ---
@site_bp.route('/')
def index():
    return render_template('index.html', username=session.get('username'))

@site_bp.route('/funcionalidades')
def funcionalidades():
    return render_template('funcionalidades.html', username=session.get('username'))

@site_bp.route('/beneficios')
def beneficios():
    return render_template('beneficios.html', username=session.get('username'))

@site_bp.route('/precos')
def precos():
    return render_template('precos.html')

@site_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')

        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('contato.html')

        try:
            msg = Message(
                subject="Nova Mensagem de Contato Hibiro 2026",
                recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            msg.body = f"Nome: {nome}\nE-mail: {email}\n\nMensagem:\n{mensagem}"
            current_app.extensions['mail'].send(msg)
            flash('Sua mensagem foi enviada com sucesso!', 'success')
            return redirect(url_for('site_bp.contato'))
        except Exception as e:
            logging.error(f"Erro e-mail: {e}")
            flash('Erro ao enviar mensagem.', 'danger')
    
    return render_template('contato.html', username=session.get('username'))

# --- FLUXO DE CADASTRO COM LOGIN AUTOMÁTICO ---

@site_bp.route('/cadastro-teste-gratis', methods=['GET'])
def cadastro_teste_gratis():
    return render_template('cadastro_teste_gratis.html')

@site_bp.route('/processar-cadastro-teste', methods=['POST'])
def processar_cadastro_teste():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    # Removi o cnpj pois sua tabela SQL usa 'id_empresa' que é um INTEGER

    if not nome or not email or not senha:
        flash('Todos os campos são obrigatórios!', 'danger')
        return redirect(url_for('site_bp.cadastro_teste_gratis'))

    db = get_db()
    
    try:
        # 1. Verificar se o e-mail já existe
        if db.execute('SELECT id FROM login_usuarios WHERE email = ?', (email,)).fetchone():
            flash('Este e-mail já está cadastrado.', 'danger')
            return redirect(url_for('site_bp.cadastro_teste_gratis'))

        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')
        
        # 2. Inserir APENAS as colunas que existem no seu SQL: id, nome, email, senha
        cursor = db.execute(
            'INSERT INTO login_usuarios (nome, email, senha) VALUES (?,?,?)',
            (nome, email, hashed_password)
        )
        new_user_id = cursor.lastrowid
        db.commit()

        # 3. LOGIN AUTOMÁTICO
        session.clear()
        session['user_id'] = new_user_id
        session['username'] = nome

        logging.info(f"Usuário {email} logado automaticamente após cadastro.")
        
        # 4. REDIRECIONAMENTO DIRETO
        return redirect(url_for('frota.dashboard'))

    except Exception as e:
        logging.error(f"ERRO CRÍTICO NO CADASTRO: {e}")
        flash('Erro técnico ao salvar. Verifique o terminal.', 'danger')
        return redirect(url_for('site_bp.cadastro_teste_gratis'))
    finally:
        db.close()