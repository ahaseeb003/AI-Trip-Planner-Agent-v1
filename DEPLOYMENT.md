# Deployment Guide: AI Trip Planner Agent

This guide covers how to deploy the AI Trip Planner to production environments.

## 1. Streamlit Community Cloud (Easiest)
1. Push your code to a GitHub repository.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Select the repository and the `app.py` file.
4. **Crucial**: Add your `.env` variables in the "Secrets" section of the Streamlit dashboard.

## 2. Docker Deployment
Create a `Dockerfile` in the root directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t trip-planner-agent .
docker run -p 8501:8501 --env-file .env trip-planner-agent
```

## 3. WhatsApp API Setup
To use the WhatsApp sharing feature:
1. Create a Meta Developer App.
2. Add the "WhatsApp" product.
3. Get your **Phone Number ID** and **Permanent Access Token**.
4. Verify your recipient number in the sandbox or go live with a production number.

## 4. Error Handling & Logging
The application uses standard Python logging. In production, consider piping logs to a service like Datadog or AWS CloudWatch.

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

The LangGraph nodes are wrapped in logic that handles API failures gracefully by providing mock data or informative error messages to the UI.
