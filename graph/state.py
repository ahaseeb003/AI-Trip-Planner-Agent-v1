from typing import Annotated, List, TypedDict, Union, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class TripState(TypedDict):
    """
    State of the trip planning agent.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    destination: str
    travel_date: str
    num_travelers: int
    starting_location: str
    transport_preference: str
    
    # Planning data
    weather_forecast: Dict[str, Any]
    transportation_options: List[Dict[str, Any]]
    attractions: List[Dict[str, Any]]
    restaurants: List[Dict[str, Any]]
    budget_breakdown: Dict[str, Any]
    itinerary: List[Dict[str, Any]]
    
    # Control flow
    next_node: str
    error: str
