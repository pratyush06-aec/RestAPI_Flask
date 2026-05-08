from PIL.ImagePalette import random
from flask import Flask, render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy 
import os, sqlite3
from model import classify_image
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__, instance_relative_config=True)
# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///classifier.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# db= SQLAlchemy(app)

from database import insert_prediction, fetch_history

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    db_path = os.path.join(app.instance_path, "classifier.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        prediction TEXT,
        confidence REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({"message": "Image Classifier API is running"})

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
    file.save(filepath)

    try:
        result = classify_image(filepath)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)



# We can change the port of our local-host by adding our customized port in our code itself