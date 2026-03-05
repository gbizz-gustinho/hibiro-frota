from flask import Blueprint, render_template, session, redirect, url_for

site_bp = Blueprint('site', __name__)

@site_bp.route('/')
def index():
    if 'username' in session: return redirect(url_for('frota.dashboard'))
    return render_template('site/index.html')

@site_bp.route('/funcionalidades')
def funcionalidades(): return render_template('site/funcionalidades.html')

@site_bp.route('/beneficios')
def beneficios(): return render_template('site/beneficios.html')

@site_bp.route('/contato')
def contato(): return render_template('site/contato.html')