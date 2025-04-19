import requests
import json

def test_search():
    print("\nTesting search endpoint with Gemini...")
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/search',
            json={
                "location": "San Francisco, CA",
                "radius": 10,  # Smaller radius for more focused results
                "activity_types": ["restaurant", "park"]
            }
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.ok:
            print("\nGemini Response:")
            data = response.json()
            if 'activities' in data:
                print(f"Found {len(data['activities'])} activities:")
                for activity in data['activities']:
                    print("\nActivity:")
                    print(f"Name: {activity.get('name', 'N/A')}")
                    print(f"Type: {activity.get('type', 'N/A')}")
                    print(f"Description: {activity.get('description', 'N/A')}")
                    print(f"Location: {activity.get('location', 'N/A')}")
                    print(f"Rating: {activity.get('rating', 'N/A')}")
            else:
                print("Unexpected response format:", json.dumps(data, indent=2))
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            print("Response Text:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Flask is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_activity_details():
    print("\nTesting activity details endpoint with Gemini...")
    try:
        # First get some activities to get a valid ID
        search_response = requests.post(
            'http://127.0.0.1:5000/api/search',
            json={
                "location": "San Francisco, CA",
                "radius": 10,
                "activity_types": ["restaurant"]
            }
        )
        
        if search_response.ok:
            activities = search_response.json().get('activities', [])
            if activities:
                # Use the first activity's name as the ID
                activity_name = activities[0]['name']
                print(f"\nGetting details for: {activity_name}")
                
                details_response = requests.get(f'http://127.0.0.1:5000/api/activity/{activity_name}')
                print(f"Status Code: {details_response.status_code}")
                
                if details_response.ok:
                    print("\nActivity Details:")
                    details = details_response.json().get('details', {})
                    print(json.dumps(details, indent=2))
                else:
                    print(f"Error getting details: {details_response.text}")
            else:
                print("No activities found to test details endpoint")
        else:
            print("Error getting activities:", search_response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Flask is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # First test if the server is running
    try:
        health_check = requests.get('http://127.0.0.1:5000/')
        if health_check.ok:
            print("Server is running!")
            test_search()
            test_activity_details()
        else:
            print("Server returned an error. Status code:", health_check.status_code)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Flask is running on http://127.0.0.1:5000") 