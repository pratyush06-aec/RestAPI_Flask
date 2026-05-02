from PIL.ImagePalette import random
from flask import Flask, render_template, request
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

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.instance_path, exist_ok=True)

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
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    if file.filename == "":
        return "No file selected"
    filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    label, confidence = classify_image(filepath)
    insert_prediction(filename, label, confidence)

    return render_template("result.html", prediction=label, confidence=confidence, image=filepath)

@app.route("/history")
def history():
    data = fetch_history()
    return render_template("history.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)



# We can change the port of our local-host by adding our customized port in our code itself