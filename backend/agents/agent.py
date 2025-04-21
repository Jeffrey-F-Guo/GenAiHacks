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

def find_places(location="San Francisco", interest="fun things", time="", date="", radius=10):
    """
    Find places or events based on user preferences.
    
    Args:
        location (str): The city or area to search in
        interest (str): The type of place or activity to find
        time (str): Time of day (morning, afternoon, evening, night)
        date (str): The date or day for the activity
        radius (int): The radius in miles to search for places around the location
        
    Returns:
        dict: A list of recommended places with their details in JSON format
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
    # return a list of places in json format
    return [
        {
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating", "No rating"),
            "types": place.get("types", [])
        }
        for place in data.get("results", [])[:4]
    ]

def format_response(raw_output):
    """
    Normalize the agent output into the expected frontend schema.
    Always returns:
    {
        "recommendations": [
            {
                "name": ...,
                "address": ...,
                "rating": ...,
                "types": [...]
            }, ...
        ]
    }
    """
    print("Raw output:", raw_output)
    
    # If raw_output is already a list (direct output from find_places)
    if isinstance(raw_output, str):
        try:
            raw_output = json.loads(raw_output)
        except json.JSONDecodeError:
            raw_output = []
    new_output = {"recommendations": raw_output}
    print("New output:", new_output)
    return new_output

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
    find_places_tool = FunctionTool.from_defaults(
        name="find_places",
        description="Find places or activities based on location, interest, time, and date",
        fn=find_places
    )

    format_response_tool = FunctionTool.from_defaults(
        name="format_response",
        description="Format a raw agent output (possibly with markdown code blocks) into a JSON object with a 'recommendations' array. This tool should always be the last one used.",
        fn=format_response
    )
    
    # Define the system prompt as part of the agent's configuration
    system_prompt = """
    You are an event recommendation assistant.
    
    The user will provide their preferences as a JSON object containing location, interest, time, date, and radius.
    Use the `find_places` tool with these parameters to get recommendations.
    The `format_response` tool should always be the last tool used to ensure the output has the correct format.
    
    Return the final JSON response that includes the recommendations array.
    """
    
    # Create ReAct agent with our tools and LLM
    agent = ReActAgent.from_tools(
        [find_places_tool, format_response_tool],
        llm=llm,
        verbose=True,
        system_prompt=system_prompt  # Pass the system prompt during agent creation
    )
    
    return agent

def run_agent(user_input: str) -> dict:
    """
    Process user input with the ReAct agent and return structured JSON.
    
    Args:
        user_input: A JSON string containing preferences (location, interest, time, date, notes)
        
    Returns:
        dict: A dictionary containing recommendations array and query info
    """
    # Parse the input JSON
    try:
        input_data = json.loads(user_input)
        location = input_data.get('location', '')
        interest = input_data.get('interest', '')
        time = input_data.get('time', '')
        date = input_data.get('date', '')
        notes = input_data.get('notes', '')
    except json.JSONDecodeError:
        return {
            'recommendations': [],
            'query': {},
            'error': 'Invalid input format'
        }

    # Set up the agent
    agent = setup_react_agent()
    
    # Create a structured prompt for the agent
    prompt = f"""Find places based on these preferences:
Location: {location}
Interest: {interest}
Time: {time}
Date: {date}
Additional Notes: {notes}

Use the find_places tool to get recommendations, then use format_response to ensure the output has the correct format.
The final response must be a JSON object with a 'recommendations' array containing place objects with name, address, rating, and types fields."""

    # Get the agent's response
    response = agent.chat(prompt)
    
    # Parse the response
    try:
        # First try direct JSON parsing
        response_data = json.loads(response.response)
        print("in the try block", response_data)
        # If it's already in the correct format, return it
        if isinstance(response_data, dict) and 'recommendations' in response_data:
            return response_data
            
        # If it's a list, wrap it in recommendations
        if isinstance(response_data, list):
            return {
                'recommendations': response_data,
                'query': {
                    'location': location,
                    'interest': interest,
                    'time': time,
                    'date': date,
                    'notes': notes
                }
            }
    except json.JSONDecodeError:
        # If parsing fails, try to extract JSON from the text
        try:
            import re
            json_match = re.search(r'\{.*\}', response.response, re.DOTALL)
            if json_match:
                response_data = json.loads(json_match.group())
                if isinstance(response_data, dict) and 'recommendations' in response_data:
                    return response_data
        except:
            pass

    # If all parsing attempts fail, return empty recommendations
    print("Failed to parse agent response")
    print(response)
    return response
    # return {
    #     'recommendations': [],
    #     'query': {
    #         'location': location,
    #         'interest': interest,
    #         'time': time,
    #         'date': date,
    #         'notes': notes
    #     },
    #     'error': 'Failed to parse agent response'
    # }