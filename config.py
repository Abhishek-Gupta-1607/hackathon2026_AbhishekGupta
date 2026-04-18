import os
from dotenv import load_dotenv

load_dotenv()

# First check standard environment variables (local .env or Streamlit Cloud Secrets)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    try:
        import streamlit as st
        # Fallback to Streamlit secrets dict if os.getenv fails to catch it
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

# The model to use for Gemini API
MODEL_NAME = "gemini-1.5-pro"
