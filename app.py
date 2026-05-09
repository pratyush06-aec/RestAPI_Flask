# from PIL.ImagePalette import random
from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy 
import os, sqlite3
from model import classify_image
from werkzeug.utils import secure_filename
import uuid
from database import insert_prediction
import traceback

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, instance_relative_config=True)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

API_KEY = os.getenv("API_KEY")

# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///classifier.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# db= SQLAlchemy(app)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

CORS(
    app,
    resources={
        r"/predict": {
            "origins": []
        }
    }
)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def init_db():
#     db_path = os.path.join(app.instance_path, "classifier.db")
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS predictions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         filename TEXT,
#         prediction TEXT,
#         confidence REAL
#     )
#     """)

#     conn.commit()
#     conn.close()

# init_db()

@app.before_request
def check_api_key():

    # print("EXPECTED:", API_KEY)
    # print("RECEIVED:", request.headers.get("x-api-key"))

    # Protect only /predict route
    if request.endpoint == "predict":

        key = request.headers.get("x-api-key")

        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

@app.route("/")
def home():
    return jsonify({"message": "Image Classifier API is running"})

@app.route("/predict", methods=["POST"])
@limiter.limit("10 per minute")
def predict():
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "Invalid file type"
        }), 400
    if "image" not in request.files:
        return jsonify({ "success": False, "error": "No image uploaded"}), 400
    
    file = request.files['image']
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
    file.save(filepath)

    try:
        result = classify_image(filepath)
        insert_prediction(filename, result["prediction"], result["confidence"], result["success"])
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        "success": False,
        "error": "File too large (max 10MB)"
    }), 413


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "success": False,
        "error": "Rate limit exceeded"
    }), 429

if __name__ == "__main__":
    app.run(debug=True, port=8000)



# We can change the port of our local-host by adding our customized port in our code itself