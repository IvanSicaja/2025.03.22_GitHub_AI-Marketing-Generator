import requests
import json

# Use your Cloud Run service URL
url = "https://ai-marketing-generator-service-141635887771.europe-west6.run.app/generate_ad"
headers = {"Content-Type": "application/json"}

# Sample payload
data = {
    "product_ID": 1002,
    "additional_description": "Limited time offer available!",
    "languages": ["English", "German"],
    "website_ad": True,
    "socialmedia_ad": True,
    "digital_ad": True,
    "text_generation": True,
    "image_generation": False,
    "image_template_path": "",
    "temperature": 0.7,
    "max_new_tokens": 500
}

# Send a POST request
response = requests.post(url, json=data, headers=headers)

# Print response
if response.status_code == 200:
    response_data = response.json()
    formatted_output = json.dumps(response_data, indent=4, ensure_ascii=False)
    print(formatted_output)
else:
    print(f"Error: {response.status_code}, Message: {response.text}")
