# app.py
import os
from flask import Flask, redirect, url_for, session
from extensions import bcrypt, mail
from database import close_connection, get_db # Importe o get_db aqui também
from rotas.site import site_bp
from rotas.auth import auth_bp
from rotas.frota import frota_bp
from rotas.configuracoes import config_bp

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'hibiro_2026_dev_key')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'gbizz.idi@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'fyzd rmaq elkh wrga')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

# Inicialização das Extensões
bcrypt.init_app(app)
mail.init_app(app)

# --- FILTROS CUSTOMIZADOS ---
@app.template_filter('format_currency')
def format_currency(value):
    try:
        if value is None: return "R$ 0,00"
        return f"R$ {float(value):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        return value

# --- GERENCIAMENTO DE CONTEXTO ---
@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

# --- PROCESSADOR DE CONTEXTO (O que faltava!) ---
# Isso faz com que variáveis globais fiquem disponíveis em TODOS os HTMLs automaticamente
@app.context_processor
def inject_globals():
    return {
        'empresa_nome': session.get('razao_social', 'Hibiro Gestão'),
        'usuario_logado': session.get('username')
    }

# --- REGISTRO DOS BLUEPRINTS ---
# Verifique se o url_prefix ajuda na organização das suas URLs
app.register_blueprint(site_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(frota_bp, url_prefix='/frota') # Adicionado prefixo para organizar
app.register_blueprint(config_bp, url_prefix='/config')

# --- ROTAS PRINCIPAIS ---
@app.route('/')
def root():
    # Se o usuário estiver logado, manda direto pro dashboard da frota
    if 'user_id' in session:
        return redirect(url_for('frota.dashboard'))
    return redirect(url_for('site_bp.index'))

if __name__ == '__main__':
    # host 0.0.0.0 permite acesso pela rede local (celular/tablet)
    app.run(debug=True, host='0.0.0.0', port=5000)