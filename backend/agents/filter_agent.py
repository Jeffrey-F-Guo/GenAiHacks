"""
Summary Agent for Activity Finder.
This agent is responsible for formatting activity data into a
consistent, user-friendly structure.
"""

class SummaryAgent:
    """
    Agent responsible for formatting and summarizing activity data.
    
    Provides methods to standardize activity information for consistent
    presentation to the user.
    """
    
    def format_results(self, activities):
        """
        Format activities into a consistent, user-friendly structure
        
        Args:
            activities (list): List of activity dictionaries
            
        Returns:
            list: Formatted activity dictionaries ready for frontend consumption
        """
        if not activities:
            return []
            
        formatted_results = []
        
        for activity in activities:
            # Format each activity consistently
            formatted_activity = {
                "id": activity.get("id"),
                "name": activity.get("name"),
                "category": activity.get("category"),
                "address": activity.get("location", {}).get("address", "Unknown"),
                "coordinates": {
                    "lat": activity.get("location", {}).get("lat"),
                    "lng": activity.get("location", {}).get("lng")
                },
                "price": self._format_price_level(activity.get("price_level", 0)),
                "price_level": activity.get("price_level", 0),  # Include numeric version for sorting
                "rating": activity.get("rating", "N/A"),
                "hours": self._format_hours(activity.get("opening_hours", [])),
                "description": activity.get("description", ""),
                "distance": self._format_distance(activity.get("distance")),
                "distance_value": activity.get("distance")  # Include numeric version for sorting
            }
            
            # Add tags based on available data
            formatted_activity["tags"] = self._generate_tags(activity)
            
            formatted_results.append(formatted_activity)
            
        return formatted_results
    
    def _format_price_level(self, price_level):
        """
        Convert numeric price level to $ symbols
        
        Args:
            price_level (int): Price level (0-4)
            
        Returns:
            str: Formatted price string
        """
        if price_level is None:
            return "Unknown"
            
        price_map = {
            0: "Free",
            1: "$",
            2: "$$",
            3: "$$$",
            4: "$$$$"
        }
        
        return price_map.get(price_level, "Unknown")
    
    def _format_hours(self, hours):
        """
        Format opening hours nicely
        
        Args:
            hours (list): List of opening hours strings
            
        Returns:
            str: Formatted hours string
        """
        if not hours or len(hours) == 0:
            return "Hours not available"
        return ", ".join(hours)
    
    def _format_distance(self, distance):
        """
        Format distance value
        
        Args:
            distance (float): Distance in kilometers
            
        Returns:
            str: Formatted distance string
        """
        if distance is None:
            return "Unknown"
            
        if distance < 1:
            # Convert to meters for distances less than 1km
            meters = round(distance * 1000)
            return f"{meters} m"
        else:
            return f"{distance:.2f} km"
    
    def _generate_tags(self, activity):
        """
        Generate relevant tags based on activity attributes
        
        Args:
            activity (dict): Activity dictionary
            
        Returns:
            list: List of relevant tags
        """
        tags = []
        
        # Add category as a tag
        if activity.get("category"):
            tags.append(activity["category"].capitalize())
        
        # Add price-based tag
        price_level = activity.get("price_level")
        if price_level == 0:
            tags.append("Free")
        elif price_level == 1:
            tags.append("Budget-friendly")
        elif price_level == 4:
            tags.append("Luxury")
        
        # Add rating-based tag
        rating = activity.get("rating")
        if rating and float(rating) >= 4.7:
            tags.append("Highly rated")
        
        # Add distance-based tag
        distance = activity.get("distance")
        if distance and distance < 1:
            tags.append("Nearby")
        
        return tags