# metadata_api.py
from flask import Flask, request, jsonify
import sqlite3
import os
import time

app = Flask(__name__)
DB_PATH = "file_metadata.db"

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_path TEXT UNIQUE,
            modified_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/store_metadata", methods=["POST"])
def store_metadata():
    data = request.json  # Expects: {"paths": ["/path/to/file1", "/path/to/file2"]}
    if not data or "paths" not in data:
        return jsonify({"error": "Missing file paths"}), 400

    paths = data["paths"]
    inserted = 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for path in paths:
        if os.path.exists(path):
            file_name = os.path.basename(path)
            modified_time = time.ctime(os.path.getmtime(path))
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO file_metadata (file_name, file_path, modified_time) VALUES (?, ?, ?)",
                    (file_name, path, modified_time)
                )
                inserted += 1
            except Exception as e:
                print(f"Error inserting metadata: {e}")

    conn.commit()
    conn.close()
    return jsonify({"message": f"{inserted} files inserted."})

if __name__ == "__main__":
    setup_db()
    app.run(port=5005)
