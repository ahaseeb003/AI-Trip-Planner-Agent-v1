import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from graph.state import TripState
from tools.weather_tool import get_weather_forecast
from tools.maps_tool import get_places_recommendations, get_transport_costs
from config.settings import settings

llm = ChatOpenAI(model=settings.MODEL_NAME, temperature=0, api_key=settings.OPENROUTER_API_KEY, base_url=settings.OPENROUTER_BASE_URL)

def plan_transportation_node(state: TripState) -> Dict[str, Any]:
    """Node to calculate transportation costs and options."""
    print("--- PLANNING TRANSPORTATION ---")
    origin = state['starting_location']
    dest = state['destination']
    pref = state['transport_preference']
    
    costs = get_transport_costs.invoke({"origin": origin, "destination": dest, "preference": pref})
    
    return {
        "transportation_options": costs.get("comparison", []),
        "messages": [AIMessage(content=f"Found transportation options from {origin} to {dest}.")]
    }

def research_destination_node(state: TripState) -> Dict[str, Any]:
    """Node to research weather and attractions."""
    print("--- RESEARCHING DESTINATION ---")
    dest = state['destination']
    date = state['travel_date']
    
    weather = get_weather_forecast.invoke({"destination": dest, "travel_date": date})
    attractions = get_places_recommendations.invoke({"destination": dest, "place_type": "tourist_attraction"})
    restaurants = get_places_recommendations.invoke({"destination": dest, "place_type": "restaurant"})
    
    return {
        "weather_forecast": weather,
        "attractions": attractions,
        "restaurants": restaurants,
        "messages": [AIMessage(content=f"Researched {dest}: weather, attractions, and restaurants found.")]
    }

def generate_itinerary_node(state: TripState) -> Dict[str, Any]:
    """Node to generate the final itinerary and budget."""
    print("--- GENERATING ITINERARY ---")
    
    prompt = f"""
    Generate a detailed day-by-day itinerary and budget breakdown for a trip to {state['destination']}.
    Travelers: {state['num_travelers']}
    Date: {state['travel_date']}
    Starting from: {state['starting_location']}
    Transport: {state['transport_preference']}
    
    Weather: {state['weather_forecast']}
    Attractions: {state['attractions']}
    Restaurants: {state['restaurants']}
    Transport Options: {state['transportation_options']}
    
    Provide the output in a structured format including:
    1. Day-by-day plan
    2. Budget breakdown (Accommodation, Food, Activities, Transport)
    3. Total cost and Per-person cost.
    """
    
    response = llm.invoke([SystemMessage(content="You are an expert travel planner."), HumanMessage(content=prompt)])
    
    return {
        "itinerary": [{"content": response.content}],
        "budget_breakdown": {"total": "Calculated in content", "per_person": "Calculated in content"},
        "messages": [response]
    }
