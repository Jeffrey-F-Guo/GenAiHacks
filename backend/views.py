"""
Views module for Activity Finder.
This file contains all API endpoints and routes for the application.
"""
from flask import request, jsonify
from agents.location_agent import LocationAgent
from agents.data_agent import DataCollectionAgent
from agents.filter_agent import FilteringAgent
from agents.summary_agent import SummaryAgent

# Initialize agents
location_agent = LocationAgent()
data_agent = DataCollectionAgent()
filter_agent = FilteringAgent()
summary_agent = SummaryAgent()

def register_routes(app):
    """Register all API routes with the Flask application
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Simple health check endpoint to verify the API is running"""
        return jsonify({
            "status": "ok",
            "message": "Activity Finder API is running"
        })
    
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        """Return available activity categories for frontend filtering options"""
        categories = [
            "food", "outdoors", "entertainment", "sports", 
            "culture", "nightlife", "shopping"
        ]
        return jsonify({"categories": categories})
    
    @app.route('/api/search', methods=['POST'])
    def search_activities():
        """Main endpoint that orchestrates all agent interactions
        
        Expected JSON payload:
        {
            "location": "New York",
            "datetime": "2025-04-19T14:00:00",
            "category": "food",  # Optional
            "radius": 10,        # Optional, default 10km
            "price_range": "1-3" # Optional
        }
        """
        try:
            # Validate request
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
                
            data = request.json
            
            # Validate required fields
            if 'location' not in data or not data['location']:
                return jsonify({"error": "Location is required"}), 400
            
            # Extract parameters
            location = data.get('location', '')
            datetime = data.get('datetime', '')
            category = data.get('category')
            radius = float(data.get('radius', 10))  # Default 10km
            price_range = data.get('price_range')
            
            # Agent Pipeline:
            
            # 1. Location Agent: Resolve location to coordinates
            app.logger.info(f"Resolving location: {location}")
            coords = location_agent.resolve_location(location)
            if not coords:
                return jsonify({"error": "Location not found or invalid"}), 400
                
            # 2. Data Collection Agent: Get activities data
            app.logger.info(f"Fetching activities near {coords}")
            activities = data_agent.get_activities(coords, datetime)
            
            # 3. Filtering Agent: Apply filters
            app.logger.info(f"Applying filters: category={category}, radius={radius}, price_range={price_range}")
            filtered_activities = filter_agent.apply_filters(
                activities,
                coords=coords,
                category=category,
                radius=radius,
                price_range=price_range
            )
            
            # 4. Summary Agent: Format results
            app.logger.info(f"Formatting {len(filtered_activities)} activities")
            formatted_results = summary_agent.format_results(filtered_activities)
            
            # Return compiled results
            return jsonify({
                "location": location,
                "coordinates": coords,
                "datetime": datetime,
                "results": formatted_results,
                "result_count": len(formatted_results)
            })
            
        except Exception as e:
            app.logger.error(f"Error in search_activities: {str(e)}")
            return jsonify({"error": str(e)}), 500