from typing import List, Dict, Any
import random

class MockSearchAgent:
    def __init__(self):
        # Sample activity data
        self.activities = [
            {
                "id": "act1",
                "name": "Golden Gate Park",
                "type": "park",
                "location": "San Francisco, CA",
                "description": "A large urban park with gardens, lakes, and museums",
                "rating": 4.8,
                "image_url": "https://example.com/golden-gate.jpg"
            },
            {
                "id": "act2",
                "name": "The Exploratorium",
                "type": "museum",
                "location": "San Francisco, CA",
                "description": "Interactive science museum with hands-on exhibits",
                "rating": 4.7,
                "image_url": "https://example.com/exploratorium.jpg"
            },
            {
                "id": "act3",
                "name": "Fisherman's Wharf",
                "type": "attraction",
                "location": "San Francisco, CA",
                "description": "Popular tourist area with seafood restaurants and shops",
                "rating": 4.5,
                "image_url": "https://example.com/fishermans-wharf.jpg"
            },
            {
                "id": "act4",
                "name": "Tartine Bakery",
                "type": "restaurant",
                "location": "San Francisco, CA",
                "description": "Famous bakery known for its bread and pastries",
                "rating": 4.6,
                "image_url": "https://example.com/tartine.jpg"
            }
        ]

    def search(self, location: str, radius: int, activity_types: List[str]) -> List[Dict[str, Any]]:
        """Mock search that returns filtered activities"""
        # Filter by activity types if specified
        filtered_activities = self.activities
        if activity_types:
            filtered_activities = [
                act for act in self.activities 
                if act["type"] in activity_types
            ]
        
        # Add some randomness to simulate different results
        random.shuffle(filtered_activities)
        return filtered_activities[:3]  # Return max 3 results

    def get_details(self, activity_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific activity"""
        for activity in self.activities:
            if activity["id"] == activity_id:
                # Add some additional details for the mock
                details = activity.copy()
                details.update({
                    "hours": "9:00 AM - 5:00 PM",
                    "address": "123 Main St, San Francisco, CA",
                    "phone": "(555) 123-4567",
                    "website": "https://example.com",
                    "reviews": [
                        {"rating": 5, "text": "Amazing place!"},
                        {"rating": 4, "text": "Great experience"}
                    ]
                })
                return details
        return {"error": "Activity not found"} 