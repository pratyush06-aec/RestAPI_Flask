<div align="center">
  <img src="logo.png" alt="RestAPI Flask Logo" width="200" style="border-radius: 10px;" />
  
  # Image Classifier REST API

  *A production-ready Flask REST API that integrates with Hugging Face's inference API to classify images and logs the results to a PostgreSQL database.*
</div>

---

## 📌 Project Overview
This project provides a robust, scalable, and secure RESTful API built with Flask. It accepts image uploads, delegates the image classification task to a state-of-the-art vision model hosted on Hugging Face (`google/vit-base-patch16-224`), and persists every prediction's result (including success, labels, and confidence scores) into a remote PostgreSQL database (Supabase). 

### ✨ Key Features
- **Machine Learning Integration**: Leverages the `huggingface_hub` for seamless integration with powerful vision models.
- **Secure Access**: The main prediction endpoint is protected via an API Key (`x-api-key` header).
- **Rate Limiting**: Utilizes `Flask-Limiter` to protect the API from spam and DDoS (30 requests/minute default, 10 requests/minute on the predict route).
- **Persistent Storage**: Connection to a PostgreSQL database using `psycopg2` to keep historical records of all predictions.
- **File Handling**: Secure file upload handling with UUID generation to avoid filename collisions and immediate cleanup after processing.
- **CORS Support**: Configured to restrict Cross-Origin Resource Sharing based on security needs.
- **Cloud Ready**: Includes a `Procfile` and `runtime.txt` tailored for seamless deployment on platforms like Heroku, Render, or Google Cloud Run.

---

## 🏗️ Architecture

1. **Client**: Sends a POST request with an image and an API key header.
2. **Flask API (`app.py`)**: 
   - Validates the API key.
   - Applies rate limiting.
   - Saves the file securely.
3. **ML Module (`model.py`)**:
   - Calls the Hugging Face Inference API.
   - Parses the JSON response to extract the top prediction and confidence score.
4. **Database Module (`database.py`)**:
   - Stores the prediction log into PostgreSQL.
5. **Cleanup**: Deletes the local image to preserve storage space.

---

## ⚙️ Setup and Installation

Follow these steps to set up the project locally for development.

### 1. Prerequisites
- Python 3.8+ (Check `runtime.txt` for exact production version)
- PostgreSQL (or an active Supabase project)
- A [Hugging Face](https://huggingface.co/) account and API key.

### 2. Clone the Repository
```bash
git clone https://github.com/pratyush06-aec/RestAPI_Flask.git
cd RestAPI_Flask
```

### 3. Create a Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables
Create a `.env` file in the root directory and add the following configuration:
```ini
# Flask Setup
API_KEY=your_secure_api_key_here

# Hugging Face Setup
HF_API_KEY=your_hugging_face_token_here

# PostgreSQL / Supabase Setup
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=5432
```

### 6. Run the Application
```bash
python app.py
```
The server will start at `http://127.0.0.1:8000`.

---

## 🚀 API Documentation

### 1. Health Check
**Endpoint:** `GET /health`  
**Description:** Used to verify if the API is running correctly.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

### 2. Classify Image
**Endpoint:** `POST /predict`  
**Description:** Uploads an image, processes it via the HF API, and returns the classification.

**Headers Required:**
- `x-api-key`: Your secure API key (defined in `.env` as `API_KEY`)

**Body (form-data):**
- `image`: The file to upload (Allowed extensions: `.png`, `.jpg`, `.jpeg`). Max size 10MB.

**Success Response (200 OK):**
```json
{
  "success": true,
  "prediction": "golden retriever",
  "confidence": 0.985
}
```

**Common Errors:**
- `401 Unauthorized`: Missing or invalid `x-api-key`.
- `400 Bad Request`: Invalid file type or no file uploaded.
- `413 Payload Too Large`: Image exceeds the 10MB limit.
- `429 Too Many Requests`: Rate limit exceeded (10 per minute max).
- `500 Internal Server Error`: Issue reaching Hugging Face or the Database.

---

## 🛠️ Project Structure

```
RestAPI_Flask/
│
├── .env                 # Environment variables (Do NOT commit)
├── .gitignore           # Git ignore file
├── Procfile             # Gunicorn deployment configuration
├── README.md            # Project documentation
├── app.py               # Main Flask application and routing
├── database.py          # Database connection and queries
├── logo.png             # Project logo
├── model.py             # HuggingFace API integration logic
├── requirements.txt     # Python dependencies
└── runtime.txt          # Python runtime version
```

---

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
