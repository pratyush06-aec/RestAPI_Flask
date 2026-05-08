import requests, os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_API_KEY"),
)

# API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
# HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def classify_image(image_path):
    # with open(image_path, "rb") as f:
    #     print("API URL:", API_URL)
    #     response = requests.post(API_URL, headers=HEADERS, data=f, timeout=60)
    #     print("FINAL URL:", response.url)
    #     print("HEADERS:", HEADERS)
    
    #     # result = response.json()

    #     print("\n===== HUGGING FACE DEBUG =====")
    # print("STATUS CODE:", response.status_code)
    # print("RAW RESPONSE:")
    # print(response.text)
    # print("==============================\n")

    # # Handle non-success responses
    # if response.status_code != 200:
    #     return {
    #         "prediction": "API Error",
    #         "confidence": 0,
    #         "details": response.text
    #     }

    # # Safely parse JSON
    # try:
    #     result = response.json()

    # except Exception as e:
    #     return {
    #         "prediction": "JSON Parse Error",
    #         "confidence": 0,
    #         "details": str(e)
    #     }

    # # Validate response structure
    # if not isinstance(result, list):
    #     return {
    #         "prediction": "Unexpected Response",
    #         "confidence": 0,
    #         "details": result
    #     }

    # top_prediction = result[0]

    # return {
    #     "label": result[0]["label"],
    #     "confidence": result[0]["score"]
    # }

    print("IMAGE PATH:", image_path)

    result = client.image_classification(
        image=image_path,
        model="google/vit-base-patch16-224"
    )

    print("HF RESULT:", result)

    top_prediction = result[0]

    return {
        "prediction": top_prediction.label,
        "confidence": top_prediction.score
    }

