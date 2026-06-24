from langgraph.graph import StateGraph, END
from graph.state import TripState
from graph.nodes import (
    plan_transportation_node,
    research_destination_node,
    generate_itinerary_node
)

def create_trip_planner_graph():
    """
    Creates and compiles the LangGraph for trip planning.
    """
    workflow = StateGraph(TripState)
    
    # Add nodes
    workflow.add_node("plan_transportation", plan_transportation_node)
    workflow.add_node("research_destination", research_destination_node)
    workflow.add_node("generate_itinerary", generate_itinerary_node)
    
    # Set entry point
    workflow.set_entry_point("plan_transportation")
    
    # Add edges
    workflow.add_edge("plan_transportation", "research_destination")
    workflow.add_edge("research_destination", "generate_itinerary")
    workflow.add_edge("generate_itinerary", END)
    
    # Compile
    return workflow.compile()
