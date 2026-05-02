from transformers import pipeline
from PIL import Image

classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224",
    device= -1
)

def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")

    results = classifier(image)

    top_result = results[0]

    label = top_result["label"]
    confidence = round(top_result["score"] * 100, 2)

    return label, confidence

