import requests
import json

url = "http://127.0.0.1:5000/generate_ad"
headers = {"Content-Type": "application/json"}
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

response = requests.post(url, json=data, headers=headers)
response_data = response.json()

# Pretty print output in the desired format
formatted_output = json.dumps(response_data, indent=4, ensure_ascii=False)
print(formatted_output)

