import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# The model to use for Gemini API
MODEL_NAME = "gemini-1.5-pro"
