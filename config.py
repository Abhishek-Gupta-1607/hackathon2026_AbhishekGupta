import os
from dotenv import load_dotenv

load_dotenv()

# We are hardcoding the API key as requested to bypass Streamlit Cloud Configuration issues and guarantee it works.
API_KEY_HACKATHON = "AIzaSyBEdjlS6Y1RfJCwlb7T7SZ8qA1TD7tFU0Y"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_API_KEY:
    try:
        import streamlit as st
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", API_KEY_HACKATHON)
    except Exception:
        GEMINI_API_KEY = API_KEY_HACKATHON

if not GEMINI_API_KEY:
    GEMINI_API_KEY = API_KEY_HACKATHON

# The model to use for Gemini API
MODEL_NAME = "gemini-1.5-pro"

