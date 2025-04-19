import requests
import json

def test_search():
    print("\nTesting search endpoint...")
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/search',
            json={
                "location": "San Francisco, CA",
                "radius": 100,
                "activity_types": ["park", "museum"]
            }
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("Response Text:", response.text)
        
        if response.ok:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Flask is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_activity_details():
    print("\nTesting activity details endpoint...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/activity/act1')
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("Response Text:", response.text)
        
        if response.ok:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            
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