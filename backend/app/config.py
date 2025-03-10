import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini AI configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-pro"  # Use the appropriate Gemini model

# Tutor settings
DEFAULT_TEMPERATURE = 0.2
DEFAULT_GRADE_LEVEL = 8
SUPPORTED_SUBJECTS = ["math", "science", "language arts", "history", "geography"]

# API settings
API_PREFIX = "/api/v1"