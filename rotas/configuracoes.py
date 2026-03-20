from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from functools import wraps
from utils.validators import validar_documento

config_bp = Blueprint('configuracoes', __name__, url_prefix='/configuracoes')

# --- 1. DECORATOR DE SEGURANÇA ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- 2. MAPA CENTRAL DE CONFIGURAÇÕES (AUXILIARES) ---
MAPA_AUXILIAR = {
    'marcas':          ('vei_marca',           'id_marca',            'nome_marca',       'Marcas de Veículos'),
    'carroceria':      ('vei_tipo_carroceria', 'id_tipo_carroceria',   'nome_tipo',        'Tipo de Carrocerias'),
    'combustivel':     ('vei_combustivel',     'id_tipo_combustivel',  'nome_combustivel', 'Combustíveis'),
    'servico_veiculo': ('vei_servico_tipo',    'id_servico',           'nome_servico',     'Tipos de Serviço'),
    'pneu_marca':      ('vei_pneu_marca',      'id_marca_pneu',       'nome_marca_pneu',  'Marca Pneu'),
    'pneu_situacao':   ('vei_pneu_situacao',   'id_situacao',          'nome_situacao',    'Situação do Pneu'),
    'pneu_servico':    ('vei_pneu_servico',    'id_servico_pneu',      'nome_servico',     'Serviço no Pneu'),
    'manut_tipo':      ('vei_manut_tipo',      'id_tipo_manutencao',   'nome_tipo',        'Tipos de Manutenção'),
    'manut_status':    ('vei_manut_status',    'id_status_manutencao', 'nome_status',      'Status de Manutenção'),
    'multa_gravidade': ('vei_multa_gravidade', 'id_gravidade',          'nome_gravidade',   'Gravidade de Multas'),
    'doc_tipo':        ('vei_doc_tipo',        'id_tipo_doc_veiculo',  'nome_documento',   'Tipos de Documento'),
    'doc_status':      ('vei_doc_status',      'id_status_doc',        'nome_status_doc',  'Status do Documento'),
    'orgao_emissor':   ('vei_orgao_emissor',   'id_orgao',             'nome_orgao',       'Órgão Emissor'),
}

# --- 3. GESTÃO DE PARCEIROS (CLIENTE/FORNECEDOR/MOTORISTA) ---

@config_bp.route('/parceiros', methods=['GET', 'POST'])
@login_required
def config_parceiros():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_clifor').strip().upper()
        tipo = request.form.get('tipo_clifor')
        doc = request.form.get('cpf_cnpj', '000.000.000-00')
        
        # Validação do Dígito Verificador (Back-end)
        if not validar_documento(doc):
            flash(f'❌ Documento {doc} inválido! Verifique os dados.', 'danger')
            return redirect(url_for('configuracoes.config_parceiros'))
        
        try:
            db.execute('''INSERT INTO cad_clifor_colab (nome_colaborador, tipo_clifor, cpf_cnpj, tipo_pessoa) 
                          VALUES (?, ?, ?, ?)''', (nome, tipo, doc, 'JURIDICA'))
            db.commit()
            flash(f'🤝 {nome} cadastrado com sucesso!', 'success')
        except Exception as e:
            flash(f'❌ Erro ao salvar: {e}', 'danger')
        return redirect(url_for('configuracoes.config_parceiros'))
    
    parceiros = db.execute('SELECT * FROM cad_clifor_colab ORDER BY nome_colaborador').fetchall()
    return render_template('config_parceiros.html', parceiros=parceiros)

@config_bp.route('/parceiros/editar/<int:id_colaborador>', methods=['GET', 'POST'])
@login_required
def editar_parceiro(id_colaborador):
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_clifor').strip().upper()
        tipo = request.form.get('tipo_clifor')
        
        db.execute('''UPDATE cad_clifor_colab SET nome_colaborador = ?, tipo_clifor = ? 
                      WHERE id_colaborador = ?''', (nome, tipo, id_colaborador))
        db.commit()
        flash('✅ Registro atualizado!', 'success')
        return redirect(url_for('configuracoes.config_parceiros'))

    res = db.execute('SELECT * FROM cad_clifor_colab WHERE id_colaborador = ?', (id_colaborador,)).fetchone()
    if not res:
        flash('❌ Parceiro não encontrado.', 'warning')
        return redirect(url_for('configuracoes.config_parceiros'))

    parceiro_formatado = {
        'id_clifor': res['id_colaborador'],
        'nome_clifor': res['nome_colaborador'],
        'tipo_clifor': res['tipo_clifor'],
        'cpf_cnpj': res['cpf_cnpj']
    }
    return render_template('config_parceiros_editar.html', parceiro=parceiro_formatado)

@config_bp.route('/parceiros/excluir/<int:id_colaborador>', methods=['POST'])
@login_required
def excluir_parceiro(id_colaborador):
    db = get_db()
    try:
        db.execute('DELETE FROM cad_clifor_colab WHERE id_colaborador = ?', (id_colaborador,))
        db.commit()
        flash('🗑️ Parceiro removido!', 'warning')
    except Exception:
        flash('❌ Impossível excluir: este parceiro possui vínculos no sistema.', 'danger')
    return redirect(url_for('configuracoes.config_parceiros'))

# --- 4. GESTÃO DE MODELOS ---

@config_bp.route('/modelos', methods=['GET', 'POST'])
@login_required
def config_modelos():
    db = get_db()
    if request.method == 'POST':
        id_marca = request.form.get('id_marca')
        nome = request.form.get('nome_modelo').strip().upper()
        db.execute('INSERT INTO vei_modelo (nome_modelo, id_marca) VALUES (?, ?)', (nome, id_marca))
        db.commit()
        flash('🚚 Modelo adicionado!', 'success')
    
    marcas = db.execute('SELECT * FROM vei_marca ORDER BY nome_marca').fetchall()
    modelos_data = db.execute('''
        SELECT m.nome_marca, mo.nome_modelo, mo.id_modelo 
        FROM vei_modelo mo 
        JOIN vei_marca m ON mo.id_marca = m.id_marca 
        ORDER BY m.nome_marca, mo.nome_modelo
    ''').fetchall()
    return render_template('config_modelos.html', marcas=marcas, modelos=modelos_data)

# --- 5. BARRAMENTO AUXILIAR GENÉRICO (Marcas, Combustíveis, etc.) ---

@config_bp.route('/auxiliar/<slug>', methods=['GET', 'POST'])
@login_required
def config_auxiliar(slug):
    if slug not in MAPA_AUXILIAR:
        return render_template('errors/404.html'), 404

    db = get_db()
    tabela, col_id, col_nome, titulo = MAPA_AUXILIAR[slug]

    if request.method == 'POST':
        novo_valor = request.form.get('nome_registro').strip().upper()
        if novo_valor:
            try:
                db.execute(f"INSERT INTO {tabela} ({col_nome}) VALUES (?)", (novo_valor,))
                db.commit()
                flash(f'✅ {titulo} adicionado!', 'success')
            except Exception as e:
                flash(f'❌ Erro ao salvar: {str(e)}', 'danger')
        return redirect(url_for('configuracoes.config_auxiliar', slug=slug))

    registros = db.execute(f"SELECT * FROM {tabela} ORDER BY {col_nome}").fetchall()
    return render_template('config_auxiliar_generico.html', 
                           registros=registros, titulo=titulo, slug=slug, 
                           col_id=col_id, col_nome=col_nome)

@config_bp.route('/auxiliar/editar/<slug>/<int:id_reg>', methods=['GET', 'POST'])
@login_required
def editar_auxiliar(slug, id_reg):
    if slug not in MAPA_AUXILIAR:
        return redirect(url_for('frota.index'))

    db = get_db()
    tabela, col_id, col_nome, titulo = MAPA_AUXILIAR[slug]

    if request.method == 'POST':
        novo_nome = request.form.get('nome_registro').strip().upper()
        try:
            db.execute(f"UPDATE {tabela} SET {col_nome} = ? WHERE {col_id} = ?", (novo_nome, id_reg))
            db.commit()
            flash(f'✅ {titulo} atualizado!', 'success')
            return redirect(url_for('configuracoes.config_auxiliar', slug=slug))
        except Exception as e:
            flash(f'❌ Erro: {e}', 'danger')

    registro = db.execute(f"SELECT * FROM {tabela} WHERE {col_id} = ?", (id_reg,)).fetchone()
    return render_template('config_auxiliar_editar.html', 
                           registro=registro, titulo=titulo, slug=slug, 
                           col_id=col_id, col_nome=col_nome)

@config_bp.route('/auxiliar/excluir/<slug>/<int:id_reg>', methods=['POST'])
@login_required
def excluir_auxiliar(slug, id_reg):
    if slug not in MAPA_AUXILIAR:
        return redirect(url_for('frota.index'))

    db = get_db()
    tabela, col_id, _, _ = MAPA_AUXILIAR[slug]
    try:
        db.execute(f"DELETE FROM {tabela} WHERE {col_id} = ?", (id_reg,))
        db.commit()
        flash('🗑️ Registro removido!', 'warning')
    except Exception:
        flash('❌ Item em uso e não pode ser excluído.', 'danger')
    return redirect(url_for('configuracoes.config_auxiliar', slug=slug))

from utils.validators import validar_documento
from utils.formatters import formatar_valor_db, formatar_data_db, formatar_taxa_db # Nossas novas ferramentas

@config_bp.route('/empresa/salvar', methods=['POST'])
@login_required
def salvar_empresa():
    db = get_db()
    
    # --- PASSO 1: Coleta dos dados crus (Strings com máscara) ---
    cnpj_cru = request.form.get('cnpj')                # Vem: "12.345.678/0001-90"
    valor_capital_cru = request.form.get('capital')    # Vem: "R$ 50.000,00"
    data_fundacao_cru = request.form.get('fundacao')   # Vem: "15/05/2010"

    # --- PASSO 2: Validação (Segurança) ---
    if not validar_documento(cnpj_cru):
        flash('❌ CNPJ inválido!', 'danger')
        return redirect(url_for('configuracoes.config_empresa'))

    # --- PASSO 3: Limpeza e Formatação (Onde as funções entram!) ---
    # Transformamos o que o usuário viu no que o banco de dados entende
    valor_final = formatar_valor_db(valor_capital_cru) # Vira: 50000.0
    data_final = formatar_data_db(data_fundacao_cru)   # Vira: "2010-05-15"

    # --- PASSO 4: Salvamento no Banco ---
    try:
        db.execute('''
            INSERT INTO cad_empresa (cnpj, capital_social, data_fundacao, nome_fantasia)
            VALUES (?, ?, ?, ?)
        ''', (cnpj_cru, valor_final, data_final, request.form.get('nome').upper()))
        
        db.commit()
        flash('✅ Dados da empresa salvos com sucesso!', 'success')
    except Exception as e:
        flash(f'❌ Erro ao gravar no banco: {e}', 'danger')

    return redirect(url_for('configuracoes.config_empresa'))