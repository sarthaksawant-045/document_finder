# models.py
import sqlite3

DB_PATH = "doc_metadata.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table to store metadata
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT,
            filename TEXT,
            filetype TEXT,
            filesize INTEGER,
            modified_at TEXT
        )
    ''')

    # FTS5 table for full-text search
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS document_text USING fts5(
            filepath,
            content
        )
    ''')

    conn.commit()
    conn.close()
