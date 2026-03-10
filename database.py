import sqlite3
import os
from flask import g

# Caminho absoluto ou relativo para o SEU banco oficial
DATABASE = os.path.join('dados', 'hibiro_frota.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Garante que não criaremos um banco vazio na pasta errada
        if not os.path.exists('dados'):
            os.makedirs('dados')
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_app_db(app):
    # Esta função apenas gerencia o fechamento da conexão
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()