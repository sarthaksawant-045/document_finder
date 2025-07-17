import faiss
import numpy as np
import os
import pickle
import requests
from vectorizer import Embedder

INDEX_PATH = "vector_store/index.faiss"
META_PATH = "vector_store/meta.pkl"
DB_API_URL = "http://127.0.0.1:5004/add_metadata"

embedder = Embedder()

def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return faiss.IndexFlatL2(384)

def save_metadata(meta):
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

def load_metadata():
    if os.path.exists(META_PATH):
        with open(META_PATH, "rb") as f:
            return pickle.load(f)
    return []

def index_documents(doc_dict):
    paths = list(doc_dict.keys())
    texts = list(doc_dict.values())

    vectors = embedder.embed_texts(texts)
    index = load_index()
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)

    meta = load_metadata()
    meta.extend(paths)
    save_metadata(meta)

    # ✅ Send to DB API after indexing
    try:
        print("📤 Sending documents to DB service...")
        res = requests.post(
            DB_API_URL,
            json={"documents": doc_dict}
        )
        print("🧠 DB response:", res.status_code, res.text)
    except Exception as e:
        print("[DB ERROR] Failed to send to DB:", e)

    return len(paths)
