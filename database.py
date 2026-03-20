import sqlite3
import os
from flask import g

# Garante que o caminho aponte para a raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'hibiro_frota.db')

def get_db():
    """Conecta ao banco hibiro_frota.db na raiz do projeto."""
    if 'db' not in g:
        # check_same_thread=False é importante para aplicações Flask
        g.db = sqlite3.connect(
            DATABASE_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_connection(exception=None):
    """Fecha a conexão com o banco ao encerrar a requisição."""
    db = g.pop('db', None)
    if db is not None:
        db.close()