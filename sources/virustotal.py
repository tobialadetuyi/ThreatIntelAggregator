import os
import requests
from dotenv import load_dotenv

load_dotenv()
VT_API_KEY = "66b5ef8bf1a51dc55ae4036f9bec8dc45924dc7846a78b156abf57bb854c8300"

def fetch_from_virustotal():
    print("[VirusTotal] Fetching data from VirusTotal...")

    headers = {
        "x-apikey": VT_API_KEY
    }

    # Sample IP addresses (replace with real dynamic input if needed)
    ip_addresses = ["8.8.8.8", "1.1.1.1"]

    results = []

    for ip in ip_addresses:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            malicious = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0)
            results.append({
                "source": "VirusTotal",
                "ip": ip,
                "threat": f"Malicious detections: {malicious}"
            })
        except Exception as e:
            results.append({
                "source": "VirusTotal",
                "ip": ip,
                "threat": f"Error: {str(e)}"
            })

    return results

