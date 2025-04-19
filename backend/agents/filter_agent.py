import math

class FilteringAgent:
    """
    Agent responsible for filtering activities based on
    user preferences such as category, price, and distance.
    """
    
    def apply_filters(self, activities, coords, category=None, radius=10, price_range=None):
        """
        Filter activities based on given criteria
        
        Args:
            activities (list): List of activity dictionaries
            coords (dict): Reference coordinates (user's location)
            category (str): Optional category to filter by
            radius (float): Maximum distance in kilometers
            price_range (str/list): Price range filter (e.g., "1-3" or [1,3])
            
        Returns:
            list: Filtered list of activities
        """
        filtered_activities = activities.copy()
        
        # Filter by category if specified
        if category:
            filtered_activities = [
                activity for activity in filtered_activities
                if activity.get("category") == category
            ]
            
        # Filter by price range if specified
        if price_range:
            min_price, max_price = self._parse_price_range(price_range)
            filtered_activities = [
                activity for activity in filtered_activities
                if min_price <= activity.get("price_level", 0) <= max_price
            ]
            
        # Calculate distance for each activity and filter by radius
        for activity in filtered_activities:
            activity_lat = activity.get("location", {}).get("lat")
            activity_lng = activity.get("location", {}).get("lng")
            
            if activity_lat and activity_lng:
                distance = self._calculate_distance(
                    coords["lat"], coords["lng"],
                    activity_lat, activity_lng
                )
                activity["distance"] = round(distance, 2)  # Add distance to activity data
            else:
                activity["distance"] = None
        
        # Filter by radius
        filtered_activities = [
            activity for activity in filtered_activities
            if activity["distance"] is None or activity["distance"] <= radius
        ]
        
        # Sort by distance
        filtered_activities.sort(key=lambda x: x.get("distance", float('inf')))
        
        return filtered_activities
    
    def _parse_price_range(self, price_range):
        """
        Parse price range into min and max values
        
        Args:
            price_range: String like "1-3" or list [1,3]
            
        Returns:
            tuple: (min_price, max_price)
        """
        if isinstance(price_range, str) and '-' in price_range:
            parts = price_range.split('-')
            try:
                return int(parts[0]), int(parts[1])
            except (ValueError, IndexError):
                return 0, 4  # Default: all price levels
        elif isinstance(price_range, list) and len(price_range) == 2:
            return price_range[0], price_range[1]
        else:
            return 0, 4  # Default: all price levels
    
    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lng1: Coordinates of first point
            lat2, lng2: Coordinates of second point
            
        Returns:
            float: Distance in kilometers
        """
        # Earth's radius in km
        R = 6371
        
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        # Differences
        d_lat = lat2_rad - lat1_rad
        d_lng = lng2_rad - lng1_rad
        
        # Haversine formula
        a = math.sin(d_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance