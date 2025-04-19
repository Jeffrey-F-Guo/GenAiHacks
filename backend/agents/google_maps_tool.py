from langchain.tools import Tool
import googlemaps

class GoogleMapsTool:
    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

    def search_places_nearby(self, query: str, location: str = "Seattle, WA") -> str:
        geocode_result = self.client.geocode(location)
        latlng = geocode_result[0]['geometry']['location']

        places_result = self.client.places(query=query, location=latlng, radius=5000)
        results = places_result.get('results', [])
        
        if not results:
            return "No results found."
        
        return "\n".join([place['name'] for place in results[:5]])

    def as_tool(self):
        return Tool(
            name="Nearby Search",
            func=lambda x: self.search_places_nearby(x),
            description="Useful for finding local places using Google Maps"
        )
