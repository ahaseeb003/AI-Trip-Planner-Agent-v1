import streamlit as st
import uuid
from graph.graph_builder import create_trip_planner_graph
from tools.whatsapp_tool import share_itinerary_whatsapp
from config.settings import settings

# Page config
st.set_page_config(page_title="AI Trip Planner", page_icon="✈️", layout="wide")

st.title("✈️ AI Trip Planner Agent")
st.markdown("Plan your next adventure with LangGraph and Streamlit.")

# Sidebar for inputs
with st.sidebar:
    st.header("Trip Details")
    destination = st.text_input("Destination", "Paris, France")
    travel_date = st.date_input("Travel Date")
    num_travelers = st.number_input("Number of Travelers", min_value=1, value=2)
    starting_location = st.text_input("Starting Location", "New York, USA")
    transport_preference = st.selectbox("Transport Preference", ["Flight", "Train", "Bus", "Car"])
    
    plan_button = st.button("Generate Itinerary", type="primary")

# Initialize session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "itinerary_ready" not in st.session_state:
    st.session_state.itinerary_ready = False

if "final_itinerary" not in st.session_state:
    st.session_state.final_itinerary = ""

# Main logic
if plan_button:
    with st.spinner("Our AI agent is researching and planning your trip..."):
        # Initialize graph
        graph = create_trip_planner_graph()
        
        # Initial state
        initial_state = {
            "messages": [],
            "destination": destination,
            "travel_date": str(travel_date),
            "num_travelers": num_travelers,
            "starting_location": starting_location,
            "transport_preference": transport_preference,
            "weather_forecast": {},
            "transportation_options": [],
            "attractions": [],
            "restaurants": [],
            "budget_breakdown": {},
            "itinerary": []
        }
        
        # Run graph
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        result = graph.invoke(initial_state, config=config)
        
        # Store results
        st.session_state.final_itinerary = result["itinerary"][0]["content"]
        st.session_state.weather = result["weather_forecast"]
        st.session_state.attractions = result["attractions"]
        st.session_state.restaurants = result["restaurants"]
        st.session_state.itinerary_ready = True

# Display results
if st.session_state.itinerary_ready:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗓️ Your Itinerary")
        st.markdown(st.session_state.final_itinerary)
        
        # WhatsApp Share
        st.divider()
        st.subheader("📲 Share via WhatsApp")
        recipient = st.text_input("Recipient Phone (with country code)", placeholder="+1234567890")
        if st.button("Share Itinerary"):
            if recipient:
                with st.spinner("Sending..."):
                    share_res = share_itinerary_whatsapp.invoke({
                        "itinerary_summary": st.session_state.final_itinerary[:1000], # WhatsApp limit
                        "recipient_phone": recipient
                    })
                    if share_res["status"] == "success":
                        st.success("Shared successfully!")
                    else:
                        st.error(f"Failed to share: {share_res['message']}")
            else:
                st.warning("Please enter a recipient phone number.")

    with col2:
        st.subheader("☀️ Weather Forecast")
        weather = st.session_state.weather
        if "forecast" in weather:
            st.info(weather["forecast"])
        else:
            st.write(weather)
            
        st.subheader("📍 Recommended Places")
        tabs = st.tabs(["Attractions", "Restaurants"])
        
        with tabs[0]:
            for attr in st.session_state.attractions:
                st.write(f"**{attr['name']}**")
                st.caption(f"Rating: {attr['rating']} | {attr['address']}")
        
        with tabs[1]:
            for rest in st.session_state.restaurants:
                st.write(f"**{rest['name']}**")
                st.caption(f"Rating: {rest['rating']} | {rest.get('cuisine', rest.get('address'))}")

else:
    st.info("Enter your trip details and click 'Generate Itinerary' to start planning.")
    
    # Show features
    st.subheader("What this agent does:")
    features = [
        "✅ **Weather Forecast**: Real-time weather data for your destination.",
        "✅ **Smart Recommendations**: Top-rated attractions and restaurants via Google Places.",
        "✅ **Cost Comparison**: Estimates for flights, trains, and more.",
        "✅ **Budgeting**: Automatic per-person cost breakdown.",
        "✅ **WhatsApp Integration**: Share your plan instantly with friends."
    ]
    for feature in features:
        st.markdown(feature)
