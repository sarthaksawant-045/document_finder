import os
import json
import requests
from flask import Flask
from embedder import scan_and_parse_documents

# ✅ Define folders to scan (use raw strings to avoid path errors)
FOLDERS_TO_SCAN = [
    r"C:\Users\Admin\OneDrive\Documents",
    os.path.join(os.path.expanduser("~"), "Downloads"),
    r"C:\Users\Admin\OneDrive\Desktop",
]

# ✅ File to store scan status
SCAN_STATUS_PATH = "../signals/scan_status.json"
INDEXER_API_URL = "http://127.0.0.1:5002/index"

app = Flask(__name__)

# ✅ Write scan status to JSON file
def write_scan_status(status):
    os.makedirs(os.path.dirname(SCAN_STATUS_PATH), exist_ok=True)
    with open(SCAN_STATUS_PATH, "w") as f:
        json.dump({"status": status}, f)

# ✅ Main function to scan and send documents
def run_auto_scan():
    print("📡 Auto-scan started...")
    total_files = {}

    for folder in FOLDERS_TO_SCAN:
        if os.path.exists(folder):
            print(f"🔍 Scanning {folder}...")
            parsed = scan_and_parse_documents(folder)
            total_files.update(parsed)
        else:
            print(f"[!] Folder not found: {folder}")

    print(f"✅ Auto-scan complete. {len(total_files)} files found.")
    write_scan_status("complete")

    # ✅ Send parsed documents to indexer
    try:
        print("📤 Sending documents to indexer service...")
        response = requests.post(INDEXER_API_URL, json={"parsed_docs": total_files})
        print(f"🧠 Indexer response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Failed to connect to indexer: {e}")

# ✅ Run scan on app startup
run_auto_scan()

@app.route("/")
def index():
    return "📚 Reader Service is running and documents were sent to the indexer."

# ✅ Start Flask server
if __name__ == "__main__":
    app.run(port=5001)
