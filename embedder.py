import os
from docx import Document
from PyPDF2 import PdfReader

def read_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"[!] Error reading TXT {file_path}: {e}")
        return ""

def read_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"[!] Error reading DOCX {file_path}: {e}")
        return ""

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"[!] Error reading PDF {file_path}: {e}")
        return ""

def parse_file(file_path):
    ext = file_path.lower()
    if ext.endswith(".txt"):
        return read_txt(file_path)
    elif ext.endswith(".docx"):
        return read_docx(file_path)
    elif ext.endswith(".pdf"):
        return read_pdf(file_path)
    else:
        print(f"[!] Unsupported file format: {file_path}")
        return None

def scan_and_parse_documents(base_dir):
    parsed_documents = {}
    print(f"📁 Scanning folder: {base_dir}")

    for root, _, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)
            if file.lower().endswith(('.txt', '.docx', '.pdf')):
                print(f"🔍 Parsing: {path}")
                text = parse_file(path)
                if text:
                    parsed_documents[path] = text
                else:
                    print(f"[!] Failed to parse: {path}")
    print("✅ Scanning and parsing complete.")
    return parsed_documents
