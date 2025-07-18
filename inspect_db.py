# inspect_db.py
import sqlite3

# abra o banco que seu alembic está usando (ajuste o nome/ caminho se necessário)
conn = sqlite3.connect("ouroboros.db")
cur = conn.cursor()

# liste as tabelas
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Tabelas:", tables)

# mostre o esquema da tabela users
cur.execute("PRAGMA table_info('users');")
schema = cur.fetchall()
print("\nEsquema de users:")
for col in schema:
    # col = (cid, name, type, notnull, dflt_value, pk)
    print(f" - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else ''} PK" if col[5] else f" - {col[1]} ({col[2]})")
