from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from agents.agent import run_agent
import json

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register the API blueprint

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Event Planning API",
        "endpoints": {
            "process_input": "POST /process_input - Process user input for event planning"
        }
    })

# predcondition: user has already selected a location, interest, time, and date
@app.route('/handle_preferences', methods=['POST'])
def handle_preferences():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    print("Received data:", data)
    stringified_json = json.dumps(data)
    # call agent to handle preferences
    response = run_agent(stringified_json)
    print("Agent response:", response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    
    