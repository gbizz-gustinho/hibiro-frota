# app.py
from flask import Flask, redirect, url_for, flash, session # Adicionei 'session' por boas práticas
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Importando os Blueprints ---
from rotas.site import site_bp
from rotas.auth import auth_bp
from rotas.frota import frota_bp
from rotas.configuracoes import config_bp

# --- Importe suas extensões e banco de dados ---
from extensions import bcrypt
from database import close_connection # <-- init_db REMOVIDO daqui

# --- Importações para Flask-Mail ---
from flask_mail import Mail, Message

# --------------------------------------------------------------------------
# Configuração Principal da Aplicação Flask
# --------------------------------------------------------------------------
app = Flask(__name__)

# --- Configurações da Aplicação ---
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'sua_chave_secreta_de_desenvolvimento_aqui') # TROQUE ESTA CHAVE!
app.config['STATIC_FOLDER'] = 'static'

# --- Configurações do Flask-Mail ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'gbizz.idi@gmail.com') # <-- SEU EMAIL AQUI
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'fyzd rmaq elkh wrga') # <-- SUA SENHA/APP PASSWORD AQUI
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'gbizz.idi@gmail.com') # <-- E-MAIL REMETENTE PADRÃO

# --- Inicialização de Extensões ---
bcrypt.init_app(app)
mail = Mail(app) # <--- Inicialização da instância Mail!

# --------------------------------------------------------------------------
# Gerenciamento de Banco de Dados
# --------------------------------------------------------------------------
@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

# --------------------------------------------------------------------------
# Filtros Personalizados para Jinja2
# --------------------------------------------------------------------------
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"

# --------------------------------------------------------------------------
# Registro dos Blueprints
# --------------------------------------------------------------------------
app.register_blueprint(site_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(frota_bp, url_prefix='/frota')
app.register_blueprint(config_bp, url_prefix='/configuracoes')

# --------------------------------------------------------------------------
# Rotas Globais / Redirecionamentos
# --------------------------------------------------------------------------
@app.route('/')
def root_redirect():
    return redirect(url_for('site_bp.index'))

# --------------------------------------------------------------------------
# Execução da Aplicação
# --------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
