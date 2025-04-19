from flask import Blueprint, request, jsonify
from .agents.search_agent import SearchAgent

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
search_agent = SearchAgent()

@api_blueprint.route('/search', methods=['POST'])
def search_activities():
    """
    Search for activities based on user parameters
    Expected JSON payload:
    {
        "location": "San Francisco, CA",
        "radius": 5000,  # in meters
        "activity_types": ["restaurant", "park", "museum"]
    }
    """
    try:
        data = request.get_json()
        
        # Required parameters
        location = data.get('location')
        radius = data.get('radius', 5000)  # Default 5km
        activity_types = data.get('activity_types', [])
        
        # Optional parameters
        max_results = data.get('max_results', 10)
        open_now = data.get('open_now', False)
        
        # Validate inputs
        if not location:
            return jsonify({"error": "Location is required"}), 400
        
        # Use the search agent to find activities
        results = search_agent.search(
            location=location,
            radius=radius,
            activity_types=activity_types,
            max_results=max_results,
            open_now=open_now
        )
        
        return jsonify({"results": results})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/activity/<activity_id>', methods=['GET'])
def get_activity_details(activity_id):
    """Get detailed information about a specific activity"""
    try:
        details = search_agent.get_details(activity_id)
        return jsonify({"details": details})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})