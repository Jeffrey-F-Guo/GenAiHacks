class SummaryAgent:
    """
    Agent responsible for formatting and summarizing activity data
    into a consistent, user-friendly structure.
    """
    
    def format_results(self, activities):
        """
        Format activities into a consistent, user-friendly structure
        
        Args:
            activities (list): List of activity dictionaries
            
        Returns:
            list: Formatted activity dictionaries
        """
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
                "rating": activity.get("rating", "N/A"),
                "hours": self._format_hours(activity.get("opening_hours", [])),
                "description": activity.get("description", ""),
                "distance": self._format_distance(activity.get("distance"))
            }
            
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
        return "$" * price_level if price_level > 0 else "Free"
    
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
        return f"{distance:.2f} km"