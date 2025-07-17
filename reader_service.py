import os
import json
import requests
from flask import Flask
from embedder import scan_and_parse_documents

# 🆕 Modular class to handle DB communication
class DatabaseAPI:
    def __init__(self, api_url: str = "http://127.0.0.1:5004/add_metadata"):
        self.api_url = api_url

    def send_metadata(self, documents: dict, timeout: int = 5) -> bool:
        if not documents:
            print("[!] No documents to send to DB.")
            return False
        try:
            print(f"📥 Sending metadata for {len(documents)} documents to DB...")
            response = requests.post(
                self.api_url,
                json={"documents": documents},
                timeout=timeout
            )
            response.raise_for_status()
            print("✅ Successfully sent metadata to DB")
            return True
        except requests.exceptions.RequestException as e:
            print(f"[!] DB API error: {e}")
            return False

# 📁 Folder Paths to Scan
USER_HOME = os.path.expanduser("~")
FOLDERS_TO_SCAN = [
    os.path.join(USER_HOME, "Documents"),
    os.path.join(USER_HOME, "Downloads"),
    os.path.join(USER_HOME, "Desktop"),
]

# 🌐 API Paths
SCAN_STATUS_PATH = "../signals/scan_status.json"
INDEXER_API_URL = "http://127.0.0.1:5002/index"
DATABASE_API_URL = "http://127.0.0.1:5004/add_metadata"

# 🔧 Flask App Init
app = Flask(__name__)
db_api = DatabaseAPI(DATABASE_API_URL)

def write_scan_status(status: str):
    os.makedirs(os.path.dirname(SCAN_STATUS_PATH), exist_ok=True)
    with open(SCAN_STATUS_PATH, "w") as f:
        json.dump({"status": status}, f)

def run_auto_scan():
    print("📡 Auto-scan started...")
    total_files = {}

    for folder in FOLDERS_TO_SCAN:
        if os.path.exists(folder):
            print(f"🔍 Scanning {folder}...")
            parsed = scan_and_parse_documents(folder)
            total_files.update(parsed)

    print(f"✅ Auto-scan complete. {len(total_files)} files found.")
    write_scan_status("complete")

    # Send to Indexer Service
    try:
        print("📤 Sending documents to indexer service...")
        response = requests.post(INDEXER_API_URL, json={"parsed_docs": total_files})
        print(f"🧠 Indexer response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Failed to connect to indexer: {e}")

    # Send to DB Service
    db_api.send_metadata(total_files)

# 🧠 Flask Routes

@app.route("/")
def index():
    return "✅ Reader Service is running."

@app.route("/scan", methods=["POST"])
def scan():
    run_auto_scan()
    return {"message": "Scan completed and data sent to indexer + DB."}, 200

@app.route("/status")
def status():
    if os.path.exists(SCAN_STATUS_PATH):
        with open(SCAN_STATUS_PATH, "r") as f:
            return json.load(f)
    return {"status": "not_started"}, 200

# 🚀 Run Flask App
if __name__ == "__main__":
    print("🚀 Reader Service is ready. Use POST /scan to trigger scanning.")
    app.run(port=5001)
