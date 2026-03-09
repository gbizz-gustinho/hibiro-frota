from flask import Blueprint, render_template, session

config_fin_bp = Blueprint('config_financeiro', __name__, url_prefix='/configuracoes/financeiro')

@config_fin_bp.route('/plano_contas')
def plano_contas():
    return render_template('errors/construcao.html', pagina="Plano de Contas", username=session.get('username'))

@config_fin_bp.route('/bancos')
def bancos():
    return render_template('errors/construcao.html', pagina="Cadastro de Bancos", username=session.get('username'))