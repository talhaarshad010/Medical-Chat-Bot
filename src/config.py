import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Gemini API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Model Configuration for Gemini
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # Medical disclaimer to append to responses
    MEDICAL_DISCLAIMER = """
    DISCLAIMER: This information is for educational purposes only.
                    designed by Usama Rasheed
    """

settings = Settings()
