from flask import Blueprint, request, jsonify
from backend.agents.agent_sim import model
import os
import json

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/search', methods=['POST'])
def search_activities():
    """
    Search for activities based on user parameters
    Expected JSON payload:
    {
        "location": "San Francisco, CA",
        "radius": 100,  # in miles
        "activity_types": ["restaurant", "park", "museum"]
    }
    """
    try:
        data = request.get_json()
        location = data.get('location')
        radius = data.get('radius', 100)
        activity_types = data.get('activity_types', [])

        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Create a natural language prompt for Gemini
        prompt = f"""
        Find fun activities in {location} within {radius} miles.
        Focus on these types of activities: {', '.join(activity_types)}.
        Return the results in JSON format with the following structure:
        {{
            "activities": [
                {{
                    "name": "Activity name",
                    "type": "Activity type",
                    "description": "Brief description",
                    "location": "Address or area",
                    "rating": "Rating if available"
                }}
            ]
        }}
        """

        # Get response from Gemini
        response = model.generate_content(prompt).text
        
        # Parse the response (Gemini should return valid JSON)
        try:
            result = json.loads(response)
            return jsonify(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse AI response"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/activity/<activity_id>', methods=['GET'])
def get_activity_details(activity_id):
    """Get detailed information about a specific activity"""
    try:
        # Create a prompt for detailed information
        prompt = f"""
        Provide detailed information about the activity with ID {activity_id}.
        Include:
        - Operating hours
        - Contact information
        - Popular times
        - User reviews
        - Any special features or requirements
        
        Return the information in JSON format.
        """
        
        response = model.generate_content(prompt).text
        try:
            details = json.loads(response)
            return jsonify({"details": details})
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse AI response"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})
