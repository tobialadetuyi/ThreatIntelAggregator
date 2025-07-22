import requests
from aggregator import ABUSEIPDB_API_KEY

def fetch_from_abuseipdb():
    print("[Aggregator] Fetching data from AbuseIPDB...")

    url = "https://api.abuseipdb.com/api/v2/blacklist"
    params = {
        "confidenceMinimum": "90",
        "limit": "10"
    }
    headers = {
        "Accept": "application/json",
        "Key": ABUSEIPDB_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json().get("data", [])
        return [
            {
                "ipAddress": entry["ipAddress"],
                "abuseConfidenceScore": entry["abuseConfidenceScore"],
                "countryCode": entry["countryCode"],
                "domain": entry.get("domain", "N/A"),
                "isp": entry.get("isp", "N/A"),
                "source": "AbuseIPDB"
            }
            for entry in result
        ]
    except requests.RequestException as e:
        print(f"[!] Error fetching from AbuseIPDB: {e}")
        return []
