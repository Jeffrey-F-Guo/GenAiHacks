"""
Data Collection Agent for Activity Finder.
This agent is responsible for fetching activity data from various sources
based on location and other parameters.
"""
import datetime

class DataCollectionAgent:
    """
    Agent responsible for collecting activity data from various sources.
    
    In a production environment, this would integrate with APIs such as
    Yelp Fusion, Google Places, Eventbrite, etc.
    """
    
    def __init__(self):
        """Initialize the DataCollectionAgent with necessary configurations"""
        # In production, you might initialize API clients here
        # For MVP, we'll use mock data
        pass
    
    def get_activities(self, coords, datetime_str=None):
        """
        Fetch activities near the given coordinates
        
        Args:
            coords (dict): Dictionary with lat and lng keys
            datetime_str (str): Optional datetime string for time-based filtering (ISO format)
            
        Returns:
            list: List of activity dictionaries
        """
        # Parse datetime if provided
        activity_datetime = None
        if datetime_str:
            try:
                activity_datetime = datetime.datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            except ValueError:
                # If datetime parsing fails, continue without time filtering
                pass
        
        # Generate mock activities around the provided coordinates
        # In production, you would make API calls here
        activities = self._generate_mock_activities(coords, activity_datetime)
        
        return activities
    
    def _generate_mock_activities(self, coords, datetime_obj=None):
        """
        Generate mock activities data for testing
        
        Args:
            coords (dict): Center coordinates
            datetime_obj (datetime): Optional datetime for time filtering
            
        Returns:
            list: List of mock activities
        """
        # Base mock activities
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
            },
            {
                "id": "8",
                "name": "Local Sports Game",
                "category": "sports",
                "location": {
                    "address": "202 Stadium Blvd",
                    "lat": coords["lat"] - 0.025,
                    "lng": coords["lng"] - 0.03
                },
                "price_level": 3,
                "rating": 4.5,
                "opening_hours": ["Varies by game schedule"],
                "description": "Professional sports event at the local stadium."
            },
            {
                "id": "9",
                "name": "Fine Dining Restaurant",
                "category": "food",
                "location": {
                    "address": "303 Gourmet Street",
                    "lat": coords["lat"] + 0.008,
                    "lng": coords["lng"] - 0.009
                },
                "price_level": 4,
                "rating": 4.9,
                "opening_hours": ["5:00 PM - 11:00 PM"],
                "description": "Upscale restaurant with award-winning chef."
            },
            {
                "id": "10",
                "name": "Modern Art Gallery",
                "category": "culture",
                "location": {
                    "address": "404 Gallery Row",
                    "lat": coords["lat"] - 0.012,
                    "lng": coords["lng"] + 0.014
                },
                "price_level": 1,
                "rating": 4.2,
                "opening_hours": ["11:00 AM - 6:00 PM"],
                "description": "Contemporary art gallery featuring local artists."
            }
        ]
        
        return mock_activities