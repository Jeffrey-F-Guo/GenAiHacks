import json
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GOOGLE_GENAI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

prompt = "I'm in San Francisco and want to go out Saturday night. Any fun ideas?"

def extract_event_preferences(prompt_text):
    """
    Uses Gemini to extract structured preferences from a user's natural language input.
    Returns a JSON dictionary with keys: location, interests, date, time_of_day
    """
    structured_prompt = f"""
You are a helpful assistant that extracts structured user preferences for event or place recommendations.

Extract the following from the user input:
- location (city or area)
- interests or types of activities if mentioned
- date or day mentioned
- time of day (morning, afternoon, evening, night) if mentioned

ONLY respond with a valid JSON object. Do not include any commentary.

User input:
\"\"\"{prompt_text}\"\"\"
"""

    try:
        response = model.generate_content(structured_prompt).text.strip()
        # print("Raw model output:\n", response)

        # Extract first valid JSON using regex
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            json_data = json.loads(match.group())
            return json_data
        else:
            raise ValueError("No valid JSON found in response.")

    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

# Test run
result = extract_event_preferences(prompt)
print("\nStructured Preferences:\n", json.dumps(result, indent=2))
