from flask import Flask, request, jsonify
import faiss
import pickle
import sqlite3
import numpy as np
from vectorizer import Embedder

app = Flask(__name__)

INDEX_PATH = "vector_storeTanmay/index.faiss"
META_PATH = "vector_storeTanmay/meta.pkl"
DB_PATH = "vector_storeTanmay/metadata.db"

embedder = Embedder()

def load_index():
    return faiss.read_index(INDEX_PATH)

def load_paths():
    with open(META_PATH, "rb") as f:
        return pickle.load(f)

def get_metadata(file_path):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM file_metadata WHERE file_path = ?", (file_path,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

@app.route("/search", methods=["POST"])
def search_documents():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing query"}), 400

    query_vector = embedder.embed([data["query"]]).astype("float32")

    index = load_index()
    file_paths = load_paths()

    D, I = index.search(query_vector, 5)

    results = []
    for dist, idx in zip(D[0], I[0]):
        if 0 <= idx < len(file_paths):
            path = file_paths[idx]
            meta = get_metadata(path)
            if meta:
                meta["score"] = float(dist)
                results.append(meta)

    return jsonify({"results": results}) if results else jsonify({"results": [], "message": "No relevant documents found."})

if __name__ == "__main__":
    app.run(debug=True)
