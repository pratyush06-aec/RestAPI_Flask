import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    # try:
    #     conn = get_connection()
    #     print("✅ Connected to Supabase")
    #     conn.close()
    # except Exception as e:
    #     print("❌ Connection error:", e)
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def insert_prediction(filename, prediction, confidence):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO predictions (filename, prediction, confidence) VALUES (%s, %s, %s)",
        (filename, prediction, confidence)
    )

    conn.commit()
    cursor.close()
    conn.close()

def fetch_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id ASC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data