import requests, os

API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def classify_image(image_path):
    with open(image_path, "rb") as f:
        response = requests.post(API_URL, headers=HEADERS, data=f)
    
    result = response.json()

    return {
        "label": result[0]["label"],
        "confidence": result[0]["score"]
    }

