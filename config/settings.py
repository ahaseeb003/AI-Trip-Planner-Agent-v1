import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    MODEL_NAME: str = os.getenv("MODEL_NAME", "google/gemini-2.0-flash-exp:free")

    # Weather API (OpenWeatherMap)
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")

    # Google Maps / Places API
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # WhatsApp Cloud API
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_RECIPIENT_PHONE: str = os.getenv("WHATSAPP_RECIPIENT_PHONE", "")

    # App Settings
    APP_NAME: str = "AI Trip Planner"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()