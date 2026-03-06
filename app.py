# app.py
from flask import Flask, redirect, url_for, flash
import os

# Importando os Blueprints (AGORA COM NOMES CONSISTENTES)
from rotas.site import site_bp          # Seu blueprint do site
from rotas.auth import auth_bp          # Seu blueprint de autenticação
from rotas.frota import frota_bp        # Seu blueprint da frota
from rotas.configuracoes import config_bp # Seu blueprint de configurações (se houver)

# Importe suas extensões e banco de dados
from extensions import bcrypt
from database import close_connection

app = Flask(__name__)
# É crucial que esta chave seja muito segura em produção
app.config['SECRET_KEY'] = 'chave_secreta_desenvolvimento_hibiro' # Mude esta chave por algo complexo e único!

# Inicializando ferramentas
bcrypt.init_app(app)

# --- GERENCIAMENTO DE BANCO DE DADOS ---
# Esta função garante que o banco seja fechado toda vez que uma página terminar de carregar
@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

# --- FILTROS PERSONALIZADOS ---
@app.template_filter('format_currency')
def format_currency(value):
    try:
        # Formatação brasileira: R$ 1.234,56
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

# --- REGISTRANDO AS ROTAS ---
app.register_blueprint(site_bp)                       # Registra o blueprint do site
app.register_blueprint(auth_bp, url_prefix='/auth')   # Registra o blueprint de autenticação com prefixo
app.register_blueprint(frota_bp, url_prefix='/frota') # Registra o blueprint da frota com prefixo
app.register_blueprint(config_bp, url_prefix='/configuracoes') # Registra o blueprint de configurações com prefixo

# Exemplo de rota de redirecionamento para a página inicial
# Esta rota raiz "/" redireciona para a rota 'index' do blueprint 'site_bp'
@app.route('/')
def root_redirect():
    return redirect(url_for('site_bp.index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
