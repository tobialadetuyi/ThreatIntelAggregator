import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def fetch_from_otx():
    """
    Fetch threat intelligence data from AlienVault OTX.
    Returns a list of dictionaries containing IPs and associated threat names.
    """
    OTX_API_KEY = os.getenv("OTX_API_KEY")  # Securely load API key from .env
    if not OTX_API_KEY:
        print("[!] OTX_API_KEY not found in environment variables.")
        return []

    print("[OTX] Fetching data from AlienVault OTX...")
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": OTX_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTP errors
        pulses = response.json().get("results", [])
        threat_data = []

        for pulse in pulses:
            for indicator in pulse.get("indicators", []):
                if indicator.get("type") == "IPv4":
                    threat_data.append({
                        "ip": indicator.get("indicator"),
                        "threat": pulse.get("name", "Unknown Threat"),
                        "source": "OTX"
                    })
        return threat_data

    except requests.RequestException as e:
        print(f"[!] Error fetching from OTX: {e}")
        return []

