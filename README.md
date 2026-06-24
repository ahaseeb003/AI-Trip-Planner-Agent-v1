# AI Trip Planner Agent ✈️

A production-ready AI Trip Planner built with **LangGraph** and **Streamlit**. This agent orchestrates multiple tools to research destinations, compare transport costs, and generate a complete itinerary with a budget breakdown.

## 🌟 Features

- **LangGraph Orchestration**: Robust workflow management for multi-step planning.
- **Weather Integration**: Get live weather forecasts for your travel dates.
- **Google Maps & Places**: Real-time recommendations for attractions and dining.
- **Budget Estimation**: Automatic calculation of total and per-person costs.
- **WhatsApp Sharing**: Send your final itinerary directly to your phone.
- **Streamlit UI**: Clean, interactive frontend for a seamless user experience.

## 📁 Project Structure

```text
ai_trip_planner/
├── app.py                # Streamlit Frontend
├── config/
│   └── settings.py       # Configuration & Environment Variables
├── graph/
│   ├── state.py          # LangGraph State Definition
│   ├── nodes.py          # Graph Nodes (Logic)
│   ├── graph_builder.py  # Graph Construction
├── tools/
│   ├── weather_tool.py   # Weather API Integration
│   ├── maps_tool.py      # Google Maps & Places Integration
│   └── whatsapp_tool.py  # WhatsApp Cloud API Integration
├── requirements.txt      # Project Dependencies
├── .env.example          # Environment Template
└── README.md             # Documentation
```

## 🚀 Getting Started

### 1. Clone and Install
```bash
git clone (https://github.com/ahaseeb003/AI-Trip-Planner-Agent-v1)
cd ai_trip_planner
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and add your API keys:
- `OPENAI_API_KEY`: For the planning agent logic.
- `OPENWEATHER_API_KEY`: For weather forecasts.
- `GOOGLE_MAPS_API_KEY`: For places and transport.
- `WHATSAPP_ACCESS_TOKEN`: For sharing features.

### 3. Run the App
```bash
streamlit run app.py
```

## 🛠️ Architecture

The agent follows a linear graph workflow:
1. **Plan Transportation**: Estimates costs based on origin and preference.
2. **Research Destination**: Fetches weather, attractions, and restaurants.
3. **Generate Itinerary**: LLM synthesizes all data into a formatted plan.

## 📝 License
MIT
