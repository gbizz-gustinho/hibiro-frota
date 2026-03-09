from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from functools import wraps

config_parceiros_bp = Blueprint('config_parceiros', __name__, url_prefix='/configuracoes/parceiros')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@config_parceiros_bp.route('/', methods=['GET', 'POST'])
@login_required
def lista():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_clifor').strip().upper()
        tipo = request.form.get('tipo_clifor')
        cpf = request.form.get('cpf_cnpj')
        db.execute('INSERT INTO cad_clifor (nome_colaborador, tipo_clifor, cpf_cnpj) VALUES (?,?,?)', (nome, tipo, cpf))
        db.commit()
        flash('Parceiro adicionado!', 'success')
    
    parceiros = db.execute('SELECT * FROM cad_clifor ORDER BY nome_colaborador').fetchall()
    return render_template('app/config_parceiros.html', parceiros=parceiros, username=session.get('username'))

@config_parceiros_bp.route('/perfil_empresa')
@login_required
def perfil_empresa():
    return render_template('app/config_empresa.html', username=session.get('username'))