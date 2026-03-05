from flask import Flask
from extensions import bcrypt

# Importando nossos Blueprints (As rotas que separamos nas pastas)
from rotas.site import site_bp
from rotas.auth import auth_bp
from rotas.frota import frota_bp
from rotas.configuracoes import config_bp

app = Flask(__name__)
app.secret_key = 'chave_secreta_desenvolvimento_hibiro'

# Inicializando a ferramenta de senhas junto com o app
bcrypt.init_app(app)

# --- FILTROS PERSONALIZADOS ---
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

# --- REGISTRANDO AS ROTAS (CONECTANDO AS PASTAS) ---
app.register_blueprint(site_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(frota_bp)
app.register_blueprint(config_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)