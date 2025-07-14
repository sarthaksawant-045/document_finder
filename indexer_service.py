from flask import Flask, request, jsonify
from indexer import index_documents

app = Flask(__name__)

@app.route("/index", methods=["POST"])
def index():
    data = request.json
    if not data or "parsed_docs" not in data:
        return jsonify({"error": "No parsed_docs provided"}), 400

    count = index_documents(data["parsed_docs"])
    return jsonify({"message": f"{count} documents indexed successfully."}), 200

if __name__ == "__main__":
    app.run(port=5002)
