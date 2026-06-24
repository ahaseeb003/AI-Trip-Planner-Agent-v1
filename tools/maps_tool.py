import requests
from langchain_core.tools import tool
from config.settings import settings

@tool
def get_places_recommendations(destination: str, place_type: str):
    """
    Recommends places (attractions or restaurants) in a destination using Google Places API.
    place_type should be 'tourist_attraction' or 'restaurant'.
    """
    if not settings.GOOGLE_MAPS_API_KEY:
        # Mock data for demonstration
        if place_type == 'tourist_attraction':
            return [
                {"name": f"Main Landmark in {destination}", "rating": 4.8, "address": "Downtown Area"},
                {"name": "Historical Museum", "rating": 4.5, "address": "Old Town"},
                {"name": "Central Park", "rating": 4.7, "address": "City Center"}
            ]
        else:
            return [
                {"name": "The Gourmet Kitchen", "rating": 4.6, "cuisine": "Local"},
                {"name": "Street Food Alley", "rating": 4.4, "cuisine": "Variety"},
                {"name": "Ocean View Dining", "rating": 4.9, "cuisine": "Seafood"}
            ]

    try:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={place_type}+in+{destination}&key={settings.GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        results = []
        for item in data.get('results', [])[:5]:
            results.append({
                "name": item.get('name'),
                "rating": item.get('rating'),
                "address": item.get('formatted_address'),
                "place_id": item.get('place_id')
            })
        return results
    except Exception as e:
        return {"error": str(e)}

@tool
def get_transport_costs(origin: str, destination: str, preference: str):
    """
    Compares transportation costs between origin and destination based on preference.
    """
    # Simplified simulation for transport costs
    base_costs = {
        "flight": 200,
        "train": 80,
        "bus": 40,
        "car": 60
    }
    
    cost = base_costs.get(preference.lower(), 100)
    
    return {
        "origin": origin,
        "destination": destination,
        "mode": preference,
        "estimated_cost_per_person": cost,
        "comparison": [
            {"mode": "Flight", "cost": 200, "duration": "2h"},
            {"mode": "Train", "cost": 80, "duration": "5h"},
            {"mode": "Bus", "cost": 40, "duration": "8h"}
        ]
    }
