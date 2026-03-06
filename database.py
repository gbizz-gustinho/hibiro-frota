import sqlite3
import os
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # 1. Pega a pasta raiz do projeto
        basedir = os.path.abspath(os.path.dirname(__file__))
        
        # 2. Aponta para o caminho correto (pasta 'dados')
        db_path = os.path.join(basedir, 'dados', 'hibiro_frota.db')
        
        # 3. Conecta e configura para retornar nomes de colunas
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row 
        
    return db

# --- ESTA É A FUNÇÃO QUE ESTAVA FALTANDO ---
def close_connection(exception=None):
    db = g.pop('_database', None)
    if db is not None:
        db.close()