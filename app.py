import os
import logging
from flask import Flask, session
from extensions import bcrypt, mail
from database import init_app_db # Agora o nome vai bater!

# IMPORTAÇÃO DOS BLUEPRINTS
from rotas.auth import auth_bp
from rotas.frota import frota_bp
from rotas.frota_bases import frota_bases_bp
from rotas.parceiros_bases import config_parceiros_bp
from rotas.site import site_bp

app = Flask(__name__)

# CONFIGURAÇÕES GERAIS
app.secret_key = 'hibiro_secret_key_2026'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# CONFIGURAÇÕES DE E-MAIL (O que estava faltando)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gbizz.idi@gmail.com' # Seu e-mail
app.config['MAIL_PASSWORD'] = 'skuw oeqa kqug pmtl' # Senha de 16 dígitos do Google
app.config['MAIL_DEFAULT_SENDER'] = 'gbizz.idi@gmail.com' # AQUI resolve o erro do log!

# INICIALIZAÇÃO DAS EXTENSÕES E BANCO
bcrypt.init_app(app)
mail.init_app(app) # DESCOMENTE ESTA LINHA para o e-mail funcionar
init_app_db(app)

# INICIALIZAÇÃO DAS EXTENSÕES E BANCO
bcrypt.init_app(app)
# Se você não for usar e-mail agora, pode comentar a linha abaixo
# mail.init_app(app) 
init_app_db(app)

# REGISTRO DE BLUEPRINTS
app.register_blueprint(site_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(frota_bp)
app.register_blueprint(frota_bases_bp)
app.register_blueprint(config_parceiros_bp)

# PROCESSADOR DE CONTEXTO (Trava de segurança da Sidebar)
@app.context_processor
def inject_user_status():
    return dict(
        perfil_completo=session.get('perfil_completo', False),
        username=session.get('username')
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=5000)