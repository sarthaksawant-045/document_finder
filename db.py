# db.py
import os
import sqlite3
from datetime import datetime
from models import DB_PATH

def insert_document_metadata(filepath, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        stats = os.stat(filepath)
        filename = os.path.basename(filepath)
        filetype = os.path.splitext(filepath)[1][1:]
        filesize = stats.st_size
        modified_at = datetime.fromtimestamp(stats.st_mtime).isoformat()

        # Insert metadata
        cursor.execute('''
            INSERT INTO documents (filepath, filename, filetype, filesize, modified_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (filepath, filename, filetype, filesize, modified_at))

        # Insert full-text content
        cursor.execute('''
            INSERT INTO document_text (filepath, content)
            VALUES (?, ?)
        ''', (filepath, content))

        conn.commit()
    except Exception as e:
        print(f"[DB Error] {e}")
    finally:
        conn.close()
