# db.py
import sqlite3

DB_NAME = 'documents.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def insert_metadata(filename, filepath, filetype, vector_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documents (filename, filepath, filetype, vector_id, embedding_status)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, filepath, filetype, vector_id, 'done' if vector_id else 'pending'))
    conn.commit()
    conn.close()

def fetch_all_documents():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents')
    results = cursor.fetchall()
    conn.close()
    return results

def get_document_by_filename(filename):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents WHERE filename = ?', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result