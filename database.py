import sqlite3

def conectar():
    conn = sqlite3.connect("rotina.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atividade TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn  