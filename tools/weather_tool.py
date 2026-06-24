import requests
from langchain_core.tools import tool
from config.settings import settings

@tool
def get_weather_forecast(destination: str, travel_date: str):
    """
    Fetches the weather forecast for a given destination and travel date.
    """
    # In a real scenario, we'd use OpenWeatherMap or similar API
    # For this project, we'll simulate the response if the key is missing
    if not settings.OPENWEATHER_API_KEY:
        return {
            "destination": destination,
            "date": travel_date,
            "forecast": "Sunny with a high of 25°C and low of 18°C. Perfect for outdoor activities.",
            "status": "Simulated (API Key missing)"
        }
    
    try:
        # Example API call structure
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={destination}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            # Process and return relevant forecast
            return data
        else:
            return {"error": f"Failed to fetch weather: {data.get('message', 'Unknown error')}"}
    except Exception as e:
        return {"error": str(e)}
