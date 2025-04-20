import json
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re
import requests
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool  


load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GOOGLE_GENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")


def find_places(preferences):
    location = preferences.get("location", "")
    interest = preferences.get("interest", "")
    time = preferences.get("time", "")
    date = preferences.get("date", "")

    query = f"{interest} in {location}"
    if time:
        query += f" during the {time}"
    if date:
        query += f" on {date}"

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    return [
        {
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating"),
            "types": place.get("types"),
        }
        for place in data.get("results", [])[:4]
    ]




def extract_preferences(prompt_text):
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

def run_agent(user_input):
    preferences = extract_preferences(user_input)
    # print("Extracted:", preferences)

    if preferences:
        results = find_places(preferences)
        
        # print("Results:", results)
        return results
    else:
        return "Sorry, I couldn't understand your request."



# preferences = {
#     "location": "San Francisco",
#     "interest": "fun things",
#     "time": "evening",
#     "date": "Saturday"
# }

# message = "I'm in San Francisco and want to go out Saturday night. Any fun ideas?";
# response = run_agent(message)
# print(response)



