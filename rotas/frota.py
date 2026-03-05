from flask import Blueprint, render_template, request, redirect, url_for, session
from database import get_db
from datetime import datetime

frota_bp = Blueprint('frota', __name__)

@frota_bp.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    stats = {
        'motoristas': db.execute('SELECT COUNT(*) FROM clifor_motorista').fetchone()[0],
        'veiculos': db.execute('SELECT COUNT(*) FROM veiculos_imobilizado_novo').fetchone()[0],
        'marcas': db.execute('SELECT COUNT(*) FROM marca_veiculo').fetchone()[0]
    }
    db.close()
    return render_template('app/dashboard.html', username=session['username'], **stats)

@frota_bp.route('/frota/lista')
def lista_frota():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    veiculos_raw = db.execute('''
        SELECT v.*, m.nome_modelo, ma.nome_marca, t.nome_tipo 
        FROM veiculos_imobilizado_novo v 
        JOIN modelo_veiculo m ON v.id_modelo = m.id_modelo 
        JOIN marca_veiculo ma ON m.id_marca = ma.id_marca
        JOIN tipo_veiculo t ON v.id_tipo = t.id_tipo
    ''').fetchall()
    db.close()
    
    hoje = datetime.now()
    processados = []
    for v in veiculos_raw:
        item = dict(v)
        if v['data_aquisicao'] and v['valor_aquisicao']:
            data = datetime.strptime(v['data_aquisicao'], '%Y-%m-%d')
            anos = (hoje - data).days / 365.25
            taxa = (v['taxa_depreciacao_anual'] or 20) / 100
            atual = v['valor_aquisicao'] - (v['valor_aquisicao'] * taxa * anos)
            item['valor_contabil_atual'] = max(atual, v['valor_aquisicao'] * 0.1)
        else:
            item['valor_contabil_atual'] = v['valor_aquisicao'] or 0
        processados.append(item)
    return render_template('app/frota_lista.html', username=session['username'], veiculos=processados)

@frota_bp.route('/frota/adicionar', methods=['GET', 'POST'])
def adicionar_veiculo():
    if 'username' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    if request.method == 'POST':
        dados = (request.form.get('placa'), request.form.get('id_modelo'), request.form.get('id_tipo'),
                 request.form.get('data_aquisicao'), request.form.get('valor_aquisicao'))
        db.execute('INSERT INTO veiculos_imobilizado_novo (placa, id_modelo, id_tipo, data_aquisicao, valor_aquisicao) VALUES (?,?,?,?,?)', dados)
        db.commit(); db.close()
        return redirect(url_for('frota.lista_frota'))
    
    marcas = db.execute('SELECT * FROM marca_veiculo').fetchall()
    tipos = db.execute('SELECT * FROM tipo_veiculo').fetchall()
    db.close()
    return render_template('app/frota_form.html', username=session['username'], marcas=marcas, tipos=tipos)