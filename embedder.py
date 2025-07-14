import os
from docx import Document
from PyPDF2 import PdfReader

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"[!] Error reading PDF {file_path}: {e}")
        return ""

def parse_file(file_path):
    if file_path.lower().endswith(".txt"):
        return read_txt(file_path)
    elif file_path.lower().endswith(".docx"):
        return read_docx(file_path)
    elif file_path.lower().endswith(".pdf"):
        return read_pdf(file_path)
    return None

def scan_and_parse_documents(base_dir):
    parsed_documents = {}
    for root, _, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)
            if file.lower().endswith(('.txt', '.docx', '.pdf')):
                text = parse_file(path)
                if text:
                    parsed_documents[path] = text
    return parsed_documents
