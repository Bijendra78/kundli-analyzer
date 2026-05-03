import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Fetch the API key from your .env file
API_KEY = os.environ.get("GEMINI_API_KEY")
# Direct REST API endpoint for the latest Gemini 2.5 Flash model
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    dob = data.get('dob')
    tob = data.get('tob')
    pob = data.get('pob')
    
    # Grab the language choice from the frontend (Defaults to English)
    language = data.get('language', 'English') 

    if not all([dob, tob, pob]):
        return jsonify({"error": "Missing birth details"}), 400

    # FIX 1: Ensure tone_instruction is always defined before the prompt
    if language == 'Hindi':
        tone_instruction = "simple, everyday conversational Hindi that normal people speak in India. Feel free to mix in common English words where appropriate (like 'Career', 'Health', 'Finance', 'Struggle'). Do NOT use pure, formal, or heavily Sanskritized Hindi. Make it extremely easy and natural to read."
    else:
        tone_instruction = "clear, professional English."

    # Fully dynamic prompt with NO hardcoded birth dates or planet positions
    prompt = f"""You are an expert Vedic astrologer. 

Birth Details: Date: {dob}, Time: {tob}, Place: {pob}

Step 1: Calculate the approximate Vedic astrological chart (Lagna, planetary positions in houses and signs) for this exact birth date and location.
Step 2: Calculate the approximate Vimshottari Dasha timeline based on the Moon's position at birth.
Step 3: Analyze the chart.

CRITICAL INSTRUCTION: Write all the descriptive text, effects, and summaries in {tone_instruction}. However, you MUST keep all the JSON keys EXACTLY in English as shown below. 

Return ONLY this exact JSON structure, filling in the empty strings with your calculated data. Do not include markdown formatting:
{{"planetaryPositions":[{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}},{{"planet":"","house":0,"sign":"","status":"","effect":""}}],"lagnaAnalysis":"","strengthsWeaknesses":"","careerFinance":"","relationships":"","healthVitality":"","dashaAnalysis":[{{"planet":"","years":"","isCurrent":false,"description":""}},{{"planet":"","years":"","isCurrent":false,"description":""}},{{"planet":"","years":"","isCurrent":true,"description":""}},{{"planet":"","years":"","isCurrent":false,"description":""}},{{"planet":"","years":"","isCurrent":false,"description":""}}],"spirituality":"","yogas":"","remedies":[{{"icon":"🟡","title":"Gemstone","description":""}},{{"icon":"🙏","title":"Mantra","description":""}},{{"icon":"🫙","title":"Charity","description":""}},{{"icon":"⚡","title":"Yantra","description":""}},{{"icon":"🌿","title":"Lifestyle","description":""}},{{"icon":"💙","title":"Saturn","description":""}}],"overallSummary":""}}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        
        if not response.ok:
            print(f"\n--- GOOGLE API ERROR ---")
            print(response.text)
            print(f"------------------------\n")
            
        response.raise_for_status() 
        
        data = response.json()
        text_response = data['candidates'][0]['content']['parts'][0]['text']
        
        # ---------------------------------------------------------
        # FIX 2: IRONCLAD JSON PARSING
        # This forces Python to only look at the text between { and }
        # ignoring any conversational text Gemini tries to add.
        # ---------------------------------------------------------
        start_idx = text_response.find('{')
        end_idx = text_response.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            clean_json = text_response[start_idx:end_idx+1]
        else:
            raise ValueError("No JSON object found in the response.")
        
        # Parse and return to frontend
        parsed_data = json.loads(clean_json)
        return jsonify(parsed_data)

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)