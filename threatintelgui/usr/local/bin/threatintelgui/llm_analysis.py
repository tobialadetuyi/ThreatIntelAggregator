import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Directly using the API key (you can change this to use os.getenv if needed)
openai.api_key = "052018413ca7b446e7a0c15ae1e3ef2f1a3855bd8c051e00ca92d4b67cdf47576bcefc93d569cfaf"

def analyze_with_llm(data, model="gpt-4"):
    enriched_data = []

    print("[DEBUG] Raw Data Sample:", data[0] if data else "No data")

    for item in data:
        ip = item.get("ip") or item.get("ipAddress", "N/A")
        threat = item.get("threat", "N/A")

        prompt = f"Classify this IP threat and provide details:\nIP: {ip}\nThreat: {threat}"

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            result = response['choices'][0]['message']['content']
            item['llm_analysis'] = result
        except Exception as e:
            item['llm_analysis'] = f"Error: {str(e)}"

        enriched_data.append(item)

    return enriched_data
