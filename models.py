# models.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        filetype TEXT,
        vector_id TEXT,
        embedding_status TEXT DEFAULT 'pending'
    )
    ''')

    conn.commit()
    conn.close()