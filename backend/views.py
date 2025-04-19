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
    """Register all API routes"""
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Simple health check endpoint"""
        return jsonify({"status": "ok"})
    
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        """Return available activity categories"""
        categories = [
            "food", "outdoors", "entertainment", "sports", 
            "culture", "nightlife", "shopping"
        ]
        return jsonify({"categories": categories})
    
    @app.route('/api/search', methods=['POST'])
    def search_activities():
        """Main endpoint that orchestrates all agent interactions"""
        try:
            data = request.json
            
            # Extract parameters
            location = data.get('location', '')
            datetime = data.get('datetime', '')
            category = data.get('category')
            radius = data.get('radius', 10)  # Default 10km/miles
            price_range = data.get('price_range')
            
            # 1. Location Agent: Resolve location to coordinates
            coords = location_agent.resolve_location(location)
            if not coords:
                return jsonify({"error": "Location not found"}), 400
                
            # 2. Data Collection Agent: Get activities data
            activities = data_agent.get_activities(coords, datetime)
            
            # 3. Filtering Agent: Apply filters
            filtered_activities = filter_agent.apply_filters(
                activities, 
                coords=coords, 
                category=category,
                radius=radius,
                price_range=price_range
            )
            
            # 4. Summary Agent: Format results
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
            return jsonify({"error": str(e)}), 500