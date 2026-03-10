from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from functools import wraps
import logging

# IMPORTAÇÃO DAS VALIDAÇÕES DO SEU UTILS
try:
    from utils.utils_format import validar_cnpj, validar_cpf
except ImportError:
    logging.error("Arquivo utils/utils_format.py não encontrado!")
    def validar_cnpj(n): return True 

config_parceiros_bp = Blueprint('parceiros_bases', __name__, url_prefix='/configuracoes/parceiros')

# --- DECORATOR DE SEGURANÇA ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# --------------------------------------------------------------------------
# 1. ROTA: LISTA E CADASTRO DE PARCEIROS (CLIENTES/FORNECEDORES)
# --------------------------------------------------------------------------
@config_parceiros_bp.route('/', methods=['GET', 'POST'])
@login_required
def lista():
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_colaborador', '').strip().upper()
        id_pessoa = request.form.get('id_pessoa')
        id_clifor_tipo = request.form.get('id_clifor')
        cpf_cnpj = request.form.get('cpf_cnpj', '')

        try:
            db.execute('''
                INSERT INTO cad_clifor (nome_colaborador, id_pessoa, id_clifor, cpf_cnpj) 
                VALUES (?, ?, ?, ?)
            ''', (nome, id_pessoa, id_clifor_tipo, cpf_cnpj))
            db.commit()
            flash(f'✅ Parceiro {nome} adicionado com sucesso!', 'success')
        except Exception as e:
            flash(f'❌ Erro ao adicionar: {e}', 'danger')
        return redirect(url_for('parceiros_bases.lista'))

    tipos_pessoa = db.execute('SELECT * FROM cad_clifor_pessoa').fetchall()
    tipos_parceiro = db.execute('SELECT * FROM cad_clifor_tipo').fetchall()
    
    parceiros = db.execute('''
        SELECT p.*, t.tipo_clifor as nome_tipo, tp.tipo_pessoa as nome_pessoa
        FROM cad_clifor p
        LEFT JOIN cad_clifor_tipo t ON p.id_clifor = t.Id_clifor
        LEFT JOIN cad_clifor_pessoa tp ON p.id_pessoa = tp.id_pessoa
        ORDER BY p.nome_colaborador
    ''').fetchall()

    return render_template('app/parceiros/config_parceiros.html', 
                            parceiros=parceiros, 
                            tipos_pessoa=tipos_pessoa, 
                            tipos_parceiro=tipos_parceiro,
                            username=session.get('username'))

# --------------------------------------------------------------------------
# 2. ROTA: EDITAR PARCEIRO
# --------------------------------------------------------------------------
@config_parceiros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_parceiro(id):
    db = get_db()
    if request.method == 'POST':
        nome = request.form.get('nome_colaborador', '').strip().upper()
        id_pessoa = request.form.get('id_pessoa')
        id_clifor = request.form.get('id_clifor')
        
        db.execute('''
            UPDATE cad_clifor SET nome_colaborador=?, id_pessoa=?, id_clifor=? 
            WHERE id_colaborador=?
        ''', (nome, id_pessoa, id_clifor, id))
        db.commit()
        flash("✅ Dados do parceiro atualizados!", "success")
        return redirect(url_for('parceiros_bases.lista'))

    parceiro = db.execute('SELECT * FROM cad_clifor WHERE id_colaborador = ?', (id,)).fetchone()
    tipos_pessoa = db.execute('SELECT * FROM cad_clifor_pessoa').fetchall()
    tipos_parceiro = db.execute('SELECT * FROM cad_clifor_tipo').fetchall()
    
    return render_template('app/parceiros/config_parceiros_edit.html', 
                           parceiro=parceiro, 
                           tipos_pessoa=tipos_pessoa, 
                           tipos_parceiro=tipos_parceiro,
                           username=session.get('username'))

# --------------------------------------------------------------------------
# 3. ROTA: PERFIL DA EMPRESA (SINCRO TOTAL COM cad_empresa.sql)
# --------------------------------------------------------------------------
@config_parceiros_bp.route('/perfil_empresa', methods=['GET', 'POST'])
@login_required
def perfil_empresa():
    db = get_db()
    usuario_id = session.get('user_id')

    if request.method == 'POST':
        cnpj_raw = request.form.get('CNPJ', '').strip()
        
        # Validação usando seu arquivo utils
        if not validar_cnpj(cnpj_raw):
            flash("❌ Erro: O CNPJ digitado é inválido!", "danger")
            return redirect(url_for('parceiros_bases.perfil_empresa'))

        # Limpeza do Capital Social para o banco DECIMAL
        cap_social = request.form.get('capital_social', '0,00')
        cap_social = cap_social.replace('R$', '').replace('.', '').replace(',', '.').strip()
        
        # MONTAGEM DA TUPLA COM TODOS OS CAMPOS DO SEU SQL
        dados = (
            request.form.get('razao_social', '').strip().upper(),
            cnpj_raw,
            request.form.get('Cep', ''),
            request.form.get('logradouro', '').upper(),
            request.form.get('numero', ''),
            request.form.get('bairro', '').upper(),
            request.form.get('municipio', '').upper(),
            request.form.get('uf', '').upper(),
            request.form.get('telefone', ''),
            request.form.get('email', '').lower(),
            request.form.get('data_abertura', ''),
            cap_social,
            request.form.get('cnae_principal', ''),
            request.form.get('ocupacao_principal', ''),
            usuario_id 
        )
        
        try:
            # UPDATE QUE BATE COM O SEU ARQUIVO cad_empresa.sql
            db.execute('''
                UPDATE cad_empresa SET 
                razao_social=?, CNPJ=?, Cep=?, logradouro=?, numero=?, 
                bairro=?, municipio=?, uf=?, telefone=?, email=?, 
                data_abertura=?, capital_social=?, cnae_principal=?, ocupacao_principal=? 
                WHERE id_usuario = ?
            ''', dados)
            db.commit()

            # Libera a Sidebar se tiver CNPJ válido
            if cnpj_raw not in ["00.000.000/0000-00", "00000000000000", ""]:
                session['perfil_completo'] = True
            
            flash("✅ Configurações da empresa salvas com sucesso!", "success")
        except Exception as e:
            logging.error(f"Erro ao salvar perfil: {e}")
            flash(f"❌ Erro ao salvar no banco: {e}", "danger")
            
        return redirect(url_for('parceiros_bases.perfil_empresa'))

    # GET: Carrega os dados para o formulário
    empresa = db.execute('SELECT * FROM cad_empresa WHERE id_usuario = ?', (usuario_id,)).fetchone()
    
    if not empresa:
        db.execute('INSERT INTO cad_empresa (id_usuario, razao_social, CNPJ) VALUES (?, ?, ?)',
                   (usuario_id, f"EMPRESA DE {session.get('username')}", "00000000000000"))
        db.commit()
        empresa = db.execute('SELECT * FROM cad_empresa WHERE id_usuario = ?', (usuario_id,)).fetchone()

    return render_template('app/parceiros/config_empresa.html', 
                           empresa=empresa, 
                           username=session.get('username'))

# --------------------------------------------------------------------------
# 4. ROTA: EXCLUIR PARCEIRO
# --------------------------------------------------------------------------
@config_parceiros_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_parceiro(id):
    db = get_db()
    db.execute('DELETE FROM cad_clifor WHERE id_colaborador = ?', (id,))
    db.commit()
    flash("🗑️ Parceiro removido!", "warning")
    return redirect(url_for('parceiros_bases.lista'))