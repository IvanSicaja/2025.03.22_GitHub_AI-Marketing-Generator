import os
from flask import Flask, request, jsonify
import pandas as pd
import requests
import json
from langchain.prompts import PromptTemplate

app = Flask(__name__)

# Load API key from an environment variable
HF_API_KEY = os.getenv("HF_API_KEY")
# Define the database path using an environment variable with a default value
CSV_DATABASE_PATH = os.getenv("CSV_DATABASE_PATH", "/mnt/database/final_product_database_with_unique_names.csv")



# Load product database
def load_product_data(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Database file not found at {csv_path}")
    df = pd.read_csv(csv_path)
    return df

# Retrieve product details from the database
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
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
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

# Main function for ad creation
def create_ad(product_ID, additional_description, languages, website_ad, socialmedia_ad, digital_ad, personalized_content, text_generation, image_generation, image_template_path, temperature=0.7, max_new_tokens=500, csv_path=CSV_DATABASE_PATH):
    df = load_product_data(csv_path)
    product_info = get_product_info(product_ID, df)

    ad_outputs = {}

    base_text = f"{product_info['name']} is a {product_info['type']} in the {product_info['category']} category. {product_info['description']} Tags: {product_info['tags']}."
    if additional_description:
        base_text += f" {additional_description}"

    for lang in languages:
        ad_outputs[lang] = {}

        # Text Ad Generation
        if text_generation:
            if website_ad:
                website_prompt = create_prompt(
                    "ONLY return an SEO-optimized product description in {language} language. DO NOT include introductions, just create the pure ad. Create decription based on:\n\n{text}",
                    language=lang, text=base_text
                )
                ad_outputs[lang]["Website Ad"] = {
                    "INPUT": website_prompt,
                    "OUTPUT": generate_text_ad(website_prompt, temperature, max_new_tokens)
                }

            if socialmedia_ad:
                socialmedia_prompt = create_prompt(
                    "ONLY return an engaging social media ad in {language} language, including 3 hashtags.DO NOT include introductions, just create the pure ad. Create decription based on:\n\n{text}",
                    language=lang, text=base_text
                )
                ad_outputs[lang]["Social Media Ad"] = {
                    "INPUT": socialmedia_prompt,
                    "OUTPUT": generate_text_ad(socialmedia_prompt, temperature, max_new_tokens)
                }

            if digital_ad:
                digital_prompt = create_prompt(
                    "ONLY return a digital ad with a strong 'Call to Action' style strictly in {language} language. DO NOT include introductions, just create the pure ad. DO NOT include HTML tags. Create description based on:\n\n{text}",
                    language=lang, text=base_text
                )
                ad_outputs[lang]["Digital Ad"] = {
                    "INPUT": digital_prompt,
                    "OUTPUT": generate_text_ad(digital_prompt, temperature, max_new_tokens)
                }

        # Image Ad Generation (Placeholder function)
        if image_generation:
            if image_template_path:
                image_prompt = create_prompt(
                    "Generate a product image for {product_name} using template {template}.",
                    product_name=product_info["name"],
                    template=image_template_path
                )
                ad_outputs[lang]["Image Ad"] = {
                    "INPUT": image_prompt,
                    "OUTPUT": f"Image generated using template: {image_template_path}"
                }
            else:
                ad_outputs[lang]["Image Ad"] = "Error: Image template path required."

    return ad_outputs

@app.route('/generate_ad', methods=['POST'])
def generate_ad():
    try:
        data = request.json

        ad_results = create_ad(
            product_ID=data["product_ID"],
            additional_description=data.get("additional_description", ""),
            languages=data.get("languages", ["English"]),
            website_ad=data.get("website_ad", True),
            socialmedia_ad=data.get("socialmedia_ad", True),
            digital_ad=data.get("digital_ad", True),
            personalized_content=data.get("personalized_content", False),
            text_generation=data.get("text_generation", True),
            image_generation=data.get("image_generation", False),
            image_template_path=data.get("image_template_path", ""),
            temperature=data.get("temperature", 0.7),
            max_new_tokens=data.get("max_new_tokens", 500)
        )

        return jsonify({"success": True, "ads": ad_results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # ❌ Debug mode disabled for production
