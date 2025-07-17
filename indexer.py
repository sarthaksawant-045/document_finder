import faiss
import numpy as np
import os
import pickle
from vectorizer import Embedder

INDEX_PATH = "vector_storeTanmay/index.faiss"
META_PATH = "vector_storeTanmay/meta.pkl"

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

    return len(paths)
