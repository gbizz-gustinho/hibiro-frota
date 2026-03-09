import os
import logging
from flask import Flask, redirect, url_for
from flask_mail import Mail

# --- Importações de Extensões e Banco ---
from extensions import bcrypt
from database import close_connection

# --- Importação dos Blueprints (O Comboio) ---
from rotas.site import site_bp
from rotas.auth import auth_bp
from rotas.frota import frota_bp
from rotas.config_parceiros import config_parceiros_bp
from rotas.config_frota import config_frota_bp
from rotas.config_financeiro import config_fin_bp

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    app = Flask(__name__)

    # --- Configurações da Máquina ---
    app.config.update(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'hibiro_2026_secret_gold'),
        STATIC_FOLDER='static',
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='gbizz.idi@gmail.com',
        MAIL_PASSWORD='fyzd rmaq elkh wrga',
        MAIL_DEFAULT_SENDER='gbizz.idi@gmail.com'
    )

    # --- Inicialização de Extensões ---
    bcrypt.init_app(app)
    Mail(app)

    # --- Gerenciamento de Banco de Dados ---
    @app.teardown_appcontext
    def teardown_db(exception):
        close_connection(exception)

    # --- Filtros Jinja2 ---
    @app.template_filter('format_currency')
    def format_currency(value):
        try:
            return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except (ValueError, TypeError):
            return "R$ 0,00"

    # --- Registro dos Blueprints (Engatando as Carretas) ---
    app.register_blueprint(site_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(frota_bp, url_prefix='/frota')
    
    # Blueprints de Configuração Separados
    app.register_blueprint(config_parceiros_bp)
    app.register_blueprint(config_frota_bp)
    app.register_blueprint(config_fin_bp)

# --- Rota Raiz ---
@app.route('/')
def root_redirect():
    return redirect(url_for('site_bp.index'))

# --- ADICIONE ESTA LINHA FORA DE QUALQUER FUNÇÃO ---
app = create_app() # O Gunicorn vai achar o 'app' aqui agora!

if __name__ == '__main__':
    # Remova a linha 'app = create_app()' daqui de dentro
    app.run(debug=True, host='0.0.0.0', port=5000)