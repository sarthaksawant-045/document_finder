# search_cli.py
import requests

API_URL = "http://127.0.0.1:5000/search"

def main():
    print("\n🔍 Enter a keyword, filename, or content to search (or 'exit' to quit):")
    while True:
        query = input("\n🔍 Search: ").strip()
        if query.lower() == 'exit':
            break

        response = requests.post(API_URL, json={"query": query})

        if response.status_code == 200:
            results = response.json().get("results", [])
            if not results:
                print("❌ No documents found.")
            else:
                print("\n✅ Top Results:")
                for idx, item in enumerate(results, start=1):
                    print(f"\n🔹 {idx}. Filename: {item['file_name']}")
                    print(f"   📁 Path: {item['file_path']}")
                    print(f"   🕒 Modified: {item['modified_at']}")
        else:
            print("❌ Error:", response.text)

if __name__ == "__main__":
    main()
