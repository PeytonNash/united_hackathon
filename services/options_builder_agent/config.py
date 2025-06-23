from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://localhost:8000"

ENDPOINTS = {
    "flight_options": "/flight_options",
    "hotel_options": "/hotel_options",
    "lounge_options": "/lounge_options",
}

GCP_PROJECT_ID = os.getenv("BQ_PROJECT")
VERTEX_MODEL = "gemini-2.5-pro"
