from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from database import get_db 

frota_bp = Blueprint('frota', __name__, url_prefix='/frota')

@frota_bp.route('/')
def dashboard():
    conn = get_db()
    
    # Busca motoristas na tabela oficial cad_clifor
    total_motoristas = conn.execute("SELECT COUNT(*) FROM cad_clifor WHERE tipo_clifor = 'MOTORISTA'").fetchone()[0]
    
    # Busca veículos na tabela oficial vei_imobilizado
    total_veiculos = conn.execute("SELECT COUNT(*) FROM vei_imobilizado WHERE status_veiculo = 'ATIVO'").fetchone()[0]

    # Gráfico: Veículos por Tipo (Carroceria)
    tipos_data = conn.execute('''
        SELECT t.nome_tipo, COUNT(v.id_veiculo) 
        FROM vei_imobilizado v 
        JOIN vei_tipo t ON v.id_tipo = t.id_tipo 
        GROUP BY t.nome_tipo
    ''').fetchall()
    
    # Gráfico: Veículos por Marca
    marcas_data = conn.execute('''
        SELECT m.nome_marca, COUNT(v.id_veiculo) 
        FROM vei_imobilizado v 
        JOIN vei_modelo mo ON v.id_modelo = mo.id_modelo 
        JOIN vei_marca m ON mo.id_marca = m.id_marca 
        GROUP BY m.nome_marca
    ''').fetchall()

    return render_template('app/dashboard.html', 
                           total_veiculos=total_veiculos,
                           total_motoristas=total_motoristas,
                           labels_tipos=[row[0] for row in tipos_data],
                           values_tipos=[row[1] for row in tipos_data],
                           labels_marcas=[row[0] for row in marcas_data],
                           values_marcas=[row[1] for row in marcas_data],
                           username="Israel Augusto")

@frota_bp.route('/lista')
def lista_frota():
    conn = get_db()
    # Query completa unindo as tabelas vei_
    veiculos_db = conn.execute('''
        SELECT v.id_veiculo, v.placa, v.data_aquisicao, v.valor_aquisicao, v.taxa_depreciacao_anual,
               m.nome_marca, mo.nome_modelo, t.nome_tipo
        FROM vei_imobilizado v
        JOIN vei_modelo mo ON v.id_modelo = mo.id_modelo
        JOIN vei_marca m ON mo.id_marca = m.id_marca
        JOIN vei_tipo t ON v.id_tipo = t.id_tipo
        ORDER BY v.placa
    ''').fetchall()

    veiculos_processados = []
    hoje = date.today()

    for v in veiculos_db:
        v_dict = dict(v)
        # Cálculo de Depreciação Contábil
        try:
            data_aq = date.fromisoformat(v_dict['data_aquisicao'])
            anos_uso = (hoje - data_aq).days / 365.25
            valor_original = v_dict['valor_aquisicao'] or 0
            taxa = (v_dict['taxa_depreciacao_anual'] or 20) / 100
            
            valor_contabil = valor_original - (valor_original * taxa * anos_uso)
            v_dict['valor_contabil_atual'] = max(valor_contabil, 0)
        except:
            v_dict['valor_contabil_atual'] = v_dict['valor_aquisicao'] or 0
            
        # Formata data para o padrão Brasil na lista
        try:
            v_dict['data_formatada'] = date.fromisoformat(v_dict['data_aquisicao']).strftime('%d/%m/%Y')
        except:
            v_dict['data_formatada'] = v_dict['data_aquisicao']

        veiculos_processados.append(v_dict)

    return render_template('app/frota_lista.html', veiculos=veiculos_processados, username="Israel Augusto")

@frota_bp.route('/adicionar', methods=['GET', 'POST'])
def adicionar_veiculo():
    conn = get_db()
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        id_modelo = request.form.get('id_modelo')
        id_tipo = request.form.get('id_tipo')
        data_aquisicao = request.form.get('data_aquisicao')
        valor_aq = request.form.get('valor_aquisicao', '0').replace(',', '.')

        try:
            conn.execute('''
                INSERT INTO vei_imobilizado (placa, id_modelo, id_tipo, data_aquisicao, valor_aquisicao, status_veiculo) 
                VALUES (?, ?, ?, ?, ?, 'ATIVO')
            ''', (placa, id_modelo, id_tipo, data_aquisicao, float(valor_aq)))
            conn.commit()
            flash('🚚 Veículo adicionado com sucesso!', 'success')
            return redirect(url_for('frota.lista_frota'))
        except Exception as e:
            flash(f'❌ Erro ao salvar: {e}', 'danger')

    modelos = conn.execute('SELECT id_modelo, nome_modelo FROM vei_modelo ORDER BY nome_modelo').fetchall()
    tipos = conn.execute('SELECT id_tipo, nome_tipo FROM vei_tipo ORDER BY nome_tipo').fetchall()
    return render_template('app/frota_adicionar.html', modelos=modelos, tipos=tipos, username="Israel Augusto")