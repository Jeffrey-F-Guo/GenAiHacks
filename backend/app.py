from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from agents.agent import run_agent

load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the API blueprint

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Event Planning API",
        "endpoints": {
            "process_input": "POST /process_input - Process user input for event planning"
        }
    })

@app.route('/process_input', methods=['POST', 'OPTIONS'])
def process_input():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    # Handle actual POST request
    try:
        user_input = request.json.get('user_input')
        print("Processing user input:", user_input)

        if not user_input:
            return jsonify({"success": False, "error": "No input provided"}), 400
        
        # Use the agent to process the input
        agent_response = run_agent(user_input)
        print("Agent response:", agent_response)
        
        # Create a simple response with the agent's text
        formatted_places = [
            {
                "name": "Agent Recommendation",
                "description": agent_response,
                "type": "agent_response",
                "rating": "N/A",
                "address": "N/A"
            }
        ]
        
        return jsonify({
            "success": True,
            "recommendations": formatted_places
        }), 200
            
    except Exception as e:
        print("Error processing input:", str(e))
        print("Traceback:", traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    
    