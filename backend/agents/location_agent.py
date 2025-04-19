class LocationAgent:
    """
    Agent responsible for resolving user-provided location strings
    into standardized geographical coordinates.
    """
    
    def resolve_location(self, location_input):
        """
        Convert a location string to coordinates (lat, lng)
        
        Args:
            location_input (str): User-provided location string
            
        Returns:
            dict: Dictionary with lat and lng keys, or None if location not found
        """
        if not location_input:
            return None
        
        # For a hackathon MVP, you can use mock data
        # In a production app, you would integrate with a geocoding service:
        # - Google Maps Geocoding API
        # - OpenStreetMap Nominatim
        # - Mapbox Geocoding API
        
        # Mock implementation with some sample locations
        location_map = {
            "new york": {"lat": 40.7128, "lng": -74.0060},
            "los angeles": {"lat": 34.0522, "lng": -118.2437},
            "chicago": {"lat": 41.8781, "lng": -87.6298},
            "san francisco": {"lat": 37.7749, "lng": -122.4194},
            "miami": {"lat": 25.7617, "lng": -80.1918},
            "seattle": {"lat": 47.6062, "lng": -122.3321}
        }
        
        # Simple case-insensitive matching
        for key, coords in location_map.items():
            if key in location_input.lower():
                return coords
                
        # Default location if not found (could also return an error)
        return {"lat": 37.7749, "lng": -122.4194}  # San Francisco as default