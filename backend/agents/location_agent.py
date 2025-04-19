"""
Location Agent for Activity Finder.
This agent is responsible for resolving user-provided location strings
into standardized geographical coordinates (latitude/longitude).
"""

class LocationAgent:
    """
    Agent responsible for resolving location strings to coordinates.
    
    In a production environment, this would integrate with a geocoding API
    such as Google Maps, OpenStreetMap Nominatim, or Mapbox.
    """
    
    def __init__(self):
        """Initialize the LocationAgent with necessary configurations"""
        # For MVP, we'll use a simple mock database of locations
        # In production, you might initialize API clients here
        self.location_database = {
            "new york": {"lat": 40.7128, "lng": -74.0060},
            "los angeles": {"lat": 34.0522, "lng": -118.2437},
            "chicago": {"lat": 41.8781, "lng": -87.6298},
            "san francisco": {"lat": 37.7749, "lng": -122.4194},
            "miami": {"lat": 25.7617, "lng": -80.1918},
            "seattle": {"lat": 47.6062, "lng": -122.3321},
            "boston": {"lat": 42.3601, "lng": -71.0589},
            "dallas": {"lat": 32.7767, "lng": -96.7970},
            "denver": {"lat": 39.7392, "lng": -104.9903},
            "austin": {"lat": 30.2672, "lng": -97.7431}
        }
    
    def resolve_location(self, location_input):
        """
        Convert a location string to coordinates (lat, lng)
        
        Args:
            location_input (str): User-provided location string
            
        Returns:
            dict: Dictionary with lat and lng keys, or None if location not found
        """
        if not location_input or not isinstance(location_input, str):
            return None
        
        # Clean the input location string
        cleaned_input = location_input.strip().lower()
        
        # Try exact match first
        if cleaned_input in self.location_database:
            return self.location_database[cleaned_input]
        
        # Try partial match
        for key, coords in self.location_database.items():
            if key in cleaned_input or cleaned_input in key:
                return coords
        
        # In a real implementation, you would call a geocoding API here if no match was found
        # For MVP, we'll return a default location
        # You could also return None or raise an exception for a location that can't be resolved
        return {"lat": 37.7749, "lng": -122.4194}  # Default to San Francisco
    
    # Future enhancement: Add method to get location suggestions based on partial input
    def get_location_suggestions(self, partial_input, max_results=5):
        """
        Get location suggestions based on partial input
        
        Args:
            partial_input (str): Partial location string
            max_results (int): Maximum number of suggestions to return
            
        Returns:
            list: List of location suggestions
        """
        if not partial_input:
            return []
            
        cleaned_input = partial_input.strip().lower()
        suggestions = []
        
        for location in self.location_database.keys():
            if cleaned_input in location:
                suggestions.append(location.title())
                if len(suggestions) >= max_results:
                    break
                    
        return suggestions