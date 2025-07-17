import requests

# Simulated indexer sending documents to your DB API
test_documents = {
    "C:/Users/Admin/Documents/example1.txt": "this is the content of file 1...",
    "C:/Users/Admin/Downloads/example2.pdf": "this is content from file 2..."
}

response = requests.post(
    "http://127.0.0.1:5004/add_metadata",
    json={"documents": test_documents}
)

print("✅ Response from DB service:", response.status_code, response.text)
