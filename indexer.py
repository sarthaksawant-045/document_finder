# indexer.py
import os
import faiss
import pickle
import requests
from embedder import Embedder  # ✅ FIXED

INDEX_PATH = "vector_storeTanmay/index.faiss"
META_PATH = "vector_storeTanmay/meta.pkl"

# ✅ Create an instance of the Embedder
embedder = Embedder()

def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        return faiss.IndexFlatL2(384)  # ✅ dimension = 384

def save_metadata(file_paths):
    with open(META_PATH, "wb") as f:
        pickle.dump(file_paths, f)

# ✅ NEW: Send metadata to Flask API
def send_metadata_to_api(file_paths):
    url = "http://localhost:5005/store_metadata"  # API you built
    try:
        response = requests.post(url, json={"paths": file_paths})
        print("🌐 Metadata API response:", response.json())
    except Exception as e:
        print(f"[!] Failed to send metadata to API: {e}")

def index_documents(doc_dict):
    print(f"🧠 Indexing {len(doc_dict)} documents...")

    paths = list(doc_dict.keys())
    texts = list(doc_dict.values())

    vectors = embedder.embed_texts(texts)  # ✅ Uses the instance

    index = load_index()
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)

    save_metadata(paths)
    send_metadata_to_api(paths)  # ✅ USE API instead of DB directly

    print("✅ Indexing complete.")
    return len(paths)
