"""
Gemini AI Service Configuration
Loads from environment variables or .env file
"""
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5003))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

SERVICE_NAME = "Gemini AI Service"
SERVICE_VERSION = "1.0.0"

SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 16000))
AUDIO_DURATION = float(os.getenv("AUDIO_DURATION", 2.0))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBuaskyXUmstXEdIDFYpWgZCwBYhHfHTpE")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")