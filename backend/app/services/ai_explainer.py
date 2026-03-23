import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def explain_all_threats(threats):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not threats:
        return threats

    # Direct URL to avoid SDK versioning bugs
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        threat_details = ""
        for i, t in enumerate(threats):
            threat_details += f"Threat {i+1}: {t['Rule']} - {t['Description']}\n"

        prompt = f"""
        You are an expert Cloud Security Engineer. Analyze these IAM vulnerabilities:
        {threat_details}
        
        Provide a concise 2-sentence explanation and one short fix for each.
        Format your response EXACTLY as a JSON list of strings: ["Explaining 1", "Explaining 2"]
        Do not include markdown blocks or any other text.
        """

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(url, json=payload)
        result = response.json()

        if "candidates" in result:
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            clean_text = raw_text.strip().replace('```json', '').replace('```', '')
            explanations = json.loads(clean_text)
            
            for i, threat in enumerate(threats):
                if i < len(explanations):
                    # This must match the key your frontend is looking for
                    threat["Explanation"] = explanations[i]
        
        return threats

    except Exception as e:
        print(f"Gemini Direct API Error: {e}")
        return threats