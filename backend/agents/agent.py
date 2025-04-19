import json
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.gemini import Gemini

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GOOGLE_GENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def find_places(location="San Francisco", interest="fun things", time="", date=""):
    """
    Find places or events based on user preferences.
    
    Args:
        location (str): The city or area to search in
        interest (str): The type of place or activity to find
        time (str): Time of day (morning, afternoon, evening, night)
        date (str): The date or day for the activity
        
    Returns:
        list: A list of recommended places with their details
    """
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
            "rating": place.get("rating", "No rating"),
            "types": place.get("types", [])
        }
        for place in data.get("results", [])[:5]
    ]

def extract_preferences(text):
    """
    Extract location, interest, time, and date from user input.
    
    Args:
        text (str): User's natural language input
        
    Returns:
        dict: Extracted preferences
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    structured_prompt = f"""
    Extract the following from the user input:
    - location (city or area)
    - interest (type of activity or place)
    - time (time of day like morning, afternoon, evening, night)
    - date (specific date or day of week)
    
    Return ONLY a valid JSON object with these keys, with empty string values if not mentioned.
    
    User input: "{text}"
    """
    
    try:
        response = model.generate_content(structured_prompt)
        json_str = response.text.strip()
        
        # Handle if the response has markdown code blocks
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
            
        preferences = json.loads(json_str)
        return preferences
    except Exception as e:
        print(f"Error extracting preferences: {e}")
        return {
            "location": "San Francisco",
            "interest": "fun things",
            "time": "",
            "date": ""
        }

def setup_react_agent():
    """
    Create and configure a ReActAgent with our tools.
    
    Returns:
        ReActAgent: Configured agent
    """
    # Create the Gemini LLM wrapper for llama_index
    llm = Gemini(
        api_key=GEMINI_API_KEY,
        model_name="gemini-1.5-pro",
        temperature=0.2
    )
    
    # Create tools
    extract_tool = FunctionTool.from_defaults(
        name="extract_preferences",
        description="Extract location, interest, time, and date preferences from user input",
        fn=extract_preferences
    )
    
    find_places_tool = FunctionTool.from_defaults(
        name="find_places",
        description="Find places or activities based on location, interest, time, and date",
        fn=find_places
    )
    
    # Create ReAct agent with our tools and LLM
    agent = ReActAgent.from_tools(
        [extract_tool, find_places_tool],
        llm=llm,
        verbose=True
    )
    
    return agent

def run_agent(user_input):
    """
    Process user input with the ReAct agent.
    
    Args:
        user_input (str): User's natural language request
        
    Returns:
        str: Agent's response with recommendations
    """
    agent = setup_react_agent()
    response = agent.chat(user_input)
    return response.response

def format_places_response(places):
    """Format the places results into a more readable response"""
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    prompt = f"""
    Create a friendly, conversational response that summarizes these place recommendations:
    {json.dumps(places, indent=2)}
    
    Include the name, address, and rating of each place in a well-formatted, easy-to-read way.
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    print("Welcome to the Places Recommendation Agent!")
    print("Ask me to find places or activities in any location.")
    print("Example: 'I'm looking for Italian restaurants in Chicago this Friday evening'")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        response = run_agent(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()