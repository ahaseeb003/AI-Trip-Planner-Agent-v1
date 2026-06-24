import requests
import json
from langchain_core.tools import tool
from config.settings import settings

@tool
def share_itinerary_whatsapp(itinerary_summary: str, recipient_phone: str = None):
    """
    Shares the trip itinerary via WhatsApp Cloud API.
    """
    phone_id = settings.WHATSAPP_PHONE_NUMBER_ID
    access_token = settings.WHATSAPP_ACCESS_TOKEN
    recipient = recipient_phone or settings.WHATSAPP_RECIPIENT_PHONE
    
    if not all([phone_id, access_token, recipient]):
        return {"status": "error", "message": "WhatsApp API credentials or recipient phone missing."}
    
    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": f"Your Trip Itinerary:\n\n{itinerary_summary}"}
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return {"status": "success", "message": "Itinerary shared via WhatsApp."}
        else:
            return {"status": "error", "message": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
