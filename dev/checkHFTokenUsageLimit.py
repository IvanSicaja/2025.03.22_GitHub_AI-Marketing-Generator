import requests
import os

# API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
# API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruuct-v0.1"
API_URL = "https://mxgcijmc07ijyyjw.eu-west-1.aws.endpoints.huggingface.cloud"

# Get the path to the current script's folder
current_folder = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the .secrets file in the same folder
secrets_path = os.path.join(current_folder, ".secrets")

# Read the token from the .secrets file
with open(secrets_path, "r") as f:
    hf_token = f.read().strip()


headers = {
    "Authorization": f"Bearer {hf_token}"
}

payload = {
    "inputs": "Hello! How can I use Hugging Face models with Python?",
    "parameters": {
        "temperature": 0.7,
        "max_new_tokens": 100,
        "top_p": 0.9
    }
}

response = requests.post(API_URL, headers=headers, json=payload)

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Raw response:", response.text)
