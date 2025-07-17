# db_api.py
from flask import Flask, request, jsonify
from models import init_db
from db import insert_document_metadata

app = Flask(__name__)
init_db()

@app.route("/add_metadata", methods=["POST"])
def add_metadata():
    data = request.json
    if not data or "documents" not in data:
        return jsonify({"error": "Missing 'documents' in request."}), 400

    for filepath, content in data["documents"].items():
        insert_document_metadata(filepath, content)

    return jsonify({"message": "Metadata saved."}), 200

if __name__ == "__main__":
    app.run(port=5004)
