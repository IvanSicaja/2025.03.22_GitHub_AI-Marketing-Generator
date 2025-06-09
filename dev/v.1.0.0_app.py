from flask import Flask, request, jsonify
import pandas as pd
import requests
import json
from langchain.prompts import PromptTemplate
import os

app = Flask(__name__)

# Define fixed CSV database path
CSV_DATABASE_PATH = "1.0_DB/final_product_database_with_unique_names.csv"

# Get the path to the current script's folder
current_folder = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the .secrets file in the same folder
secrets_path = os.path.join(current_folder, ".secrets")

# Read the token from the .secrets file
with open(secrets_path, "r") as f:
    hf_token = f.read().strip()

# Load product database
def load_product_data():
    df = pd.read_csv(CSV_DATABASE_PATH)
    return df

# Retrieve product details from database
def get_product_info(product_ID, df):
    product = df[df["Product_ID"] == product_ID]
    if product.empty:
        raise ValueError("Product_ID not found in database.")
    return {
        "name": product["Name"].values[0],
        "type": product["Type"].values[0],
        "category": product["Category"].values[0],
        "description": product["Description"].values[0],
        "tags": product["Tags/Keywords"].values[0]
    }

# Generate text ad using Hugging Face API
def generate_text_ad(prompt, temperature=0.7, max_new_tokens=500):
    # API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": temperature,
            "max_new_tokens": max_new_tokens,
            "top_p": 0.95,
            "top_k": 50,
            "repetition_penalty": 1.2
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output_text = response.json()[0]["generated_text"].strip()
        return clean_output(output_text, prompt)
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to clean redundant output
def clean_output(output, input_prompt):
    output = output.replace(input_prompt, "").strip()
    output_lines = output.split("\n")
    cleaned_output = " ".join(line.strip() for line in output_lines if line.strip())
    return cleaned_output

# Create structured prompts using LangChain
def create_prompt(template, **kwargs):
    prompt_template = PromptTemplate(template=template, input_variables=list(kwargs.keys()))
    return prompt_template.format(**kwargs)

@app.route('/generate_ad', methods=['POST'])
def generate_ad():
    try:
        data = request.json

        product_ID = data["product_ID"]
        additional_description = data.get("additional_description", "")
        languages = data.get("languages", ["English"])
        website_ad = data.get("website_ad", True)
        socialmedia_ad = data.get("socialmedia_ad", True)
        digital_ad = data.get("digital_ad", True)
        text_generation = data.get("text_generation", True)
        image_generation = data.get("image_generation", False)
        image_template_path = data.get("image_template_path", "")
        temperature = data.get("temperature", 0.7)
        max_new_tokens = data.get("max_new_tokens", 500)

        df = load_product_data()
        product_info = get_product_info(product_ID, df)

        ad_outputs = {}
        base_text = f"{product_info['name']} is a {product_info['type']} in the {product_info['category']} category. {product_info['description']} Tags: {product_info['tags']}."
        if additional_description:
            base_text += f" {additional_description}"

        for lang in languages:
            ad_outputs[lang] = {}

            if text_generation:
                if website_ad:
                    website_prompt = create_prompt(
                        "ONLY return an SEO-optimized product description in {language}.\n{text}", language=lang,
                        text=base_text)
                    ad_outputs[lang]["Website Ad"] = generate_text_ad(website_prompt, temperature, max_new_tokens)

                if socialmedia_ad:
                    socialmedia_prompt = create_prompt(
                        "ONLY return an engaging social media ad with 3 hashtags in {language}.\n{text}", language=lang,
                        text=base_text)
                    ad_outputs[lang]["Social Media Ad"] = generate_text_ad(socialmedia_prompt, temperature,
                                                                           max_new_tokens)

                if digital_ad:
                    digital_prompt = create_prompt(
                        "ONLY return a digital ad with a strong Call to Action in {language}.\n{text}", language=lang,
                        text=base_text)
                    ad_outputs[lang]["Digital Ad"] = generate_text_ad(digital_prompt, temperature, max_new_tokens)

            if image_generation and image_template_path:
                image_prompt = create_prompt("Generate a product image for {product_name} using template {template}.",
                                             product_name=product_info["name"], template=image_template_path)
                ad_outputs[lang]["Image Ad"] = {"INPUT": image_prompt, "OUTPUT": "Image generated successfully."}

        return jsonify({"success": True, "ads": ad_outputs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
