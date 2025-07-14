# api.py
from flask import Flask, request, jsonify
from models import create_tables
from db import insert_metadata, fetch_all_documents, get_document_by_filename

app = Flask(__name__)

create_tables()  # Ensure DB table is created on server start

@app.route('/add-metadata', methods=['POST'])
def add_metadata():
    data = request.get_json()
    filename = data.get('filename')
    filepath = data.get('filepath')
    filetype = data.get('filetype')
    vector_id = data.get('vector_id')

    if not filename or not filepath:
        return jsonify({'error': 'filename and filepath are required'}), 400

    insert_metadata(filename, filepath, filetype, vector_id)
    return jsonify({'status': 'inserted'}), 201

@app.route('/documents', methods=['GET'])
def get_all():
    docs = fetch_all_documents()
    return jsonify([{
        'id': row[0],
        'filename': row[1],
        'filepath': row[2],
        'filetype': row[3],
        'vector_id': row[4],
        'embedding_status': row[5]
    } for row in docs])

@app.route('/document/<filename>', methods=['GET'])
def get_by_filename(filename):
    row = get_document_by_filename(filename)
    if not row:
        return jsonify({'error': 'not found'}), 404
    return jsonify({
        'id': row[0],
        'filename': row[1],
        'filepath': row[2],
        'filetype': row[3],
        'vector_id': row[4],
        'embedding_status': row[5]
    })

if __name__ == '__main__':
    app.run(port=5003)
