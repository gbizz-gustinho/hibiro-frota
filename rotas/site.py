from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import logging
from flask_mail import Message 
# Importamos o objeto 'mail' das extensões para ele funcionar aqui
from extensions import mail 

# Padronizamos o nome do Blueprint para 'site' para bater com seus url_for
site_bp = Blueprint('site', __name__, template_folder='../templates/site')

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

@site_bp.route('/precos')
def precos():
    return render_template('precos.html')

# --------------------------------------------------------------------------
# ROTA DE CONTATO
# --------------------------------------------------------------------------
@site_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email_cliente = request.form.get('email')
        mensagem = request.form.get('mensagem')

        try:
            # O objeto 'mail' agora está disponível via importação acima
            msg = Message(subject=f"Novo Contato: {nome}",
                          recipients=['gbizz.idi@gmail.com'],
                          body=f"De: {nome} <{email_cliente}>\n\n{mensagem}")
            mail.send(msg)

            # Agora o flash vai aparecer pois o HTML tem o receptor
            flash("✅ Sua mensagem foi enviada com sucesso! Responderemos em breve.", "success")
            
        except Exception as e:
            logging.error(f"Erro e-mail: {e}")
            flash(f"❌ Erro ao enviar mensagem. Tente novamente mais tarde.", "danger")

        # Usamos 'site.contato' pois o Blueprint agora se chama 'site'
        return redirect(url_for('site.contato'))

    return render_template('contato.html')

# --------------------------------------------------------------------------
# ROTAS DE CADASTRO
# --------------------------------------------------------------------------

@site_bp.route('/cadastro-teste-gratis')
def cadastro_teste_gratis():
    return render_template('cadastro_teste_gratis.html')