import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def explain_all_threats(threats):
    """
    Sends all detected threats to Gemini in a single batch to get 
    security explanations and fixes.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not threats:
        return threats

    # Direct URL to interact with Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        # Prepare the list of threats for the AI prompt
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

        # Execute the request to the Google Generative AI endpoint
        response = requests.post(url, json=payload)
        result = response.json()

        if "candidates" in result:
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # IMPROVED: Find the JSON list bounds to ignore any extra text from the AI
            try:
                start_idx = raw_text.find('[')
                end_idx = raw_text.rfind(']') + 1
                
                if start_idx != -1 and end_idx != 0:
                    clean_text = raw_text[start_idx:end_idx]
                    explanations = json.loads(clean_text)
                    
                    # Map the AI explanations back to the original threat list
                    for i, threat in enumerate(threats):
                        if i < len(explanations):
                            threat["Explanation"] = explanations[i]
                else:
                    print("Could not find JSON list in AI response.")
                    
            except json.JSONDecodeError as e:
                print(f"JSON Parsing Error: {e}. Raw text: {raw_text}")
        
        return threats

    except Exception as e:
        print(f"Gemini Direct API Error: {e}")
        return threats