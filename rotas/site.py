# rotas/site.py
from flask import Blueprint, render_template, request, flash, redirect, url_for

# Defina o Blueprint com o nome 'site_bp'
site_bp = Blueprint('site_bp', __name__)

@site_bp.route('/')
def index():
    return render_template('site/index.html')

@site_bp.route('/funcionalidades')
def funcionalidades():
    return render_template('site/funcionalidades.html')

@site_bp.route('/beneficios')
def beneficios():
    return render_template('site/beneficios.html')

@site_bp.route('/contato')
def contato():
    return render_template('site/contato.html')
            
# --- NOVA ROTA PARA EXIBIR O FORMULÁRIO DE TESTE GRÁTIS ---
@site_bp.route('/cadastro-teste-gratis')
def cadastro_teste_gratis():
    return render_template('site/cadastro_teste_gratis.html')

# --- NOVA ROTA PARA PROCESSAR O CADASTRO DO TESTE GRÁTIS ---
@site_bp.route('/processar-cadastro-teste', methods=['POST'])
def processar_cadastro_teste():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # TODO: AQUI VOCÊ IMPLEMENTARIA A LÓGICA REAL:
        # 1. Validar os dados
        # 2. Criar uma nova conta de usuário no banco de dados (marcada como "teste")
        # 3. Gerar um token de ativação/confirmar e-mail
        # 4. Enviar e-mail de boas-vindas/ativação
        # 5. Redirecionar para o login ou diretamente para a área restrita
        
        # Por enquanto, apenas um flash message e redirecionamento de exemplo:
        flash(f'Obrigado {nome}! Sua conta de teste para {email} foi criada com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('auth.login')) # auth.login é do blueprint de auth, então está correto
    return redirect(url_for('site_bp.cadastro_teste_gratis')) # Redireciona para a própria página de cadastro
