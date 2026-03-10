import sqlite3
import os

db_path = os.path.join('dados', 'hibiro_frota.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🧹 Limpando tabelas de acesso...")
cursor.execute("DELETE FROM login_usuarios")
cursor.execute("DELETE FROM cad_empresa")
# Reseta os contadores de ID para começar do 1
cursor.execute("DELETE FROM sqlite_sequence WHERE name='login_usuarios'")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='cad_empresa'")

conn.commit()
conn.close()
print("✅ Sistema pronto para novos cadastros!")