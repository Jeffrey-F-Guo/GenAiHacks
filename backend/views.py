from flask import Blueprint, request, jsonify
from agents.search_agent import SearchAgent
import os

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Initialize the real search agent
search_agent = SearchAgent(maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"))

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

        # Combine into a natural language query for the agent
        query = f"Find {', '.join(activity_types)} within {radius} miles of {location}"
        result = search_agent.run(query)
        return jsonify({"results": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/activity/<activity_id>', methods=['GET'])
def get_activity_details(activity_id):
    """Stub for future: Get detailed info on a specific activity"""
    # Currently, SearchAgent doesn’t have a get_details method, but you can add it later
    return jsonify({"details": f"Details for activity {activity_id} not implemented yet."})

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})
