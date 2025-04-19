class DataCollectionAgent:
    """
    Agent responsible for collecting activity data from various sources
    based on location and other parameters.
    """
    
    def get_activities(self, coords, datetime=None):
        """
        Fetch activities near the given coordinates
        
        Args:
            coords (dict): Dictionary with lat and lng keys
            datetime (str): Optional datetime string for time-based filtering
            
        Returns:
            list: List of activity dictionaries
        """
        # For MVP, we'll use mock data
        # In a production app, you would integrate with APIs like:
        # - Yelp Fusion API
        # - Google Places API
        # - Eventbrite API
        # - TripAdvisor API
        
        # Generate mock activities around the provided coordinates
        mock_activities = [
            {
                "id": "1",
                "name": "Central Park Walking Tour",
                "category": "outdoors",
                "location": {
                    "address": "Central Park, New York",
                    "lat": coords["lat"] + 0.01,
                    "lng": coords["lng"] - 0.01
                },
                "price_level": 1,
                "rating": 4.5,
                "opening_hours": ["9:00 AM - 5:00 PM"],
                "description": "Guided tour through the historic Central Park."
            },
            {
                "id": "2",
                "name": "Metropolitan Museum of Art",
                "category": "culture",
                "location": {
                    "address": "1000 5th Ave, New York",
                    "lat": coords["lat"] - 0.02,
                    "lng": coords["lng"] + 0.01
                },
                "price_level": 2,
                "rating": 4.8,
                "opening_hours": ["10:00 AM - 5:30 PM"],
                "description": "World-class art museum with extensive collections."
            },
            {
                "id": "3",
                "name": "Broadway Show",
                "category": "entertainment",
                "location": {
                    "address": "Times Square, New York",
                    "lat": coords["lat"] + 0.015,
                    "lng": coords["lng"] + 0.02
                },
                "price_level": 4,
                "rating": 4.7,
                "opening_hours": ["7:00 PM - 10:00 PM"],
                "description": "Live theatrical performance on Broadway."
            },
            {
                "id": "4",
                "name": "Local Coffee Shop",
                "category": "food",
                "location": {
                    "address": "123 Coffee Lane",
                    "lat": coords["lat"] - 0.01,
                    "lng": coords["lng"] - 0.02
                },
                "price_level": 2,
                "rating": 4.3,
                "opening_hours": ["6:00 AM - 8:00 PM"],
                "description": "Cozy café with specialty coffee and pastries."
            },
            {
                "id": "5",
                "name": "City Bike Tour",
                "category": "outdoors",
                "location": {
                    "address": "456 Bike Avenue",
                    "lat": coords["lat"] + 0.02,
                    "lng": coords["lng"] + 0.03
                },
                "price_level": 3,
                "rating": 4.6,
                "opening_hours": ["10:00 AM - 4:00 PM"],
                "description": "Guided bicycle tour of city highlights."
            },
            {
                "id": "6",
                "name": "Rooftop Bar",
                "category": "nightlife",
                "location": {
                    "address": "789 Sky View",
                    "lat": coords["lat"] - 0.03,
                    "lng": coords["lng"] + 0.02
                },
                "price_level": 3,
                "rating": 4.4,
                "opening_hours": ["4:00 PM - 2:00 AM"],
                "description": "Trendy rooftop bar with city views."
            },
            {
                "id": "7",
                "name": "Shopping Mall",
                "category": "shopping",
                "location": {
                    "address": "101 Retail Road",
                    "lat": coords["lat"] + 0.025,
                    "lng": coords["lng"] - 0.015
                },
                "price_level": 2,
                "rating": 4.0,
                "opening_hours": ["10:00 AM - 9:00 PM"],
                "description": "Large shopping center with various stores."
            }
        ]
        
        return mock_activities