# ✅ db_inserter.py (Used only by db_api.py — no test data)
# Location: document_finder/db_inserter.py

import os
import sqlite3
from datetime import datetime

# Use absolute path to always write DB in same folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "doc_metadata.db")

# Step 1: Initialize DB schema (FTS5 + Metadata table)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for basic metadata
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

# Step 2: Insert one document's metadata + content
def insert_document_metadata(filepath: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        stats = os.stat(filepath)
        filename = os.path.basename(filepath)
        filetype = os.path.splitext(filepath)[1][1:]
        filesize = stats.st_size
        modified_at = datetime.fromtimestamp(stats.st_mtime).isoformat()

        # Insert into metadata table
        cursor.execute('''
            INSERT INTO documents (filepath, filename, filetype, filesize, modified_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (filepath, filename, filetype, filesize, modified_at))

        # Insert into FTS5 table
        cursor.execute('''
            INSERT INTO document_text (filepath, content)
            VALUES (?, ?)
        ''', (filepath, content))

        conn.commit()
        print(f"✅ Inserted: {filename}")

    except Exception as e:
        print(f"[DB ERROR] Failed for {filepath} → {e}")

    finally:
        conn.close()

# Step 3: Bulk insert dictionary of {filepath: content}
def bulk_insert(documents: dict):
    print(f"\n📥 Inserting {len(documents)} documents into DB...")
    for path, text in documents.items():
        insert_document_metadata(path, text)
    print("✅ All documents inserted.\n")
