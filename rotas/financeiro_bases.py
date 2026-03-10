from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps

# Definição do Blueprint
config_fin_bp = Blueprint('config_financeiro', __name__, url_prefix='/configuracoes/financeiro')

# --- DECORATOR DE SEGURANÇA ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --------------------------------------------------------------------------
# ROTA: PLANO DE CONTAS
# Local: templates/app/financeiro/construcao.html
# --------------------------------------------------------------------------
@config_fin_bp.route('/plano_contas')
@login_required
def plano_contas():
    return render_template('app/financeiro/construcao.html', 
                           pagina="Plano de Contas", 
                           username=session.get('username'))

# --------------------------------------------------------------------------
# ROTA: CADASTRO DE BANCOS
# Local: templates/app/financeiro/construcao.html
# --------------------------------------------------------------------------
@config_fin_bp.route('/bancos')
@login_required
def bancos():
    return render_template('app/financeiro/construcao.html', 
                           pagina="Cadastro de Bancos", 
                           username=session.get('username'))