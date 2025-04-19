import requests
import json
import time
from datetime import datetime, timedelta

# Base URL for your API
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print("\n---\n")

def test_categories():
    """Test the categories endpoint"""
    response = requests.get(f"{BASE_URL}/categories")
    print("Categories Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print("\n---\n")

def test_search():
    """Test the search endpoint with various parameters"""
    
    # Test case 1: Basic search
    payload = {
        "location": "New York",
        "datetime": "2025-04-19T14:00:00"
    }
    response = requests.post(f"{BASE_URL}/search", json=payload)
    print("Search Response (Basic):", response.status_code)
    print(f"Found {response.json().get('result_count', 0)} activities")
    print(json.dumps(response.json(), indent=2)[:500] + "..." if len(json.dumps(response.json())) > 500 else json.dumps(response.json(), indent=2))
    print("\n---\n")
    
    # Test case 2: Search with category filter
    payload = {
        "location": "New York",
        "datetime": "2025-04-19T14:00:00",
        "category": "outdoor"
    }
    response = requests.post(f"{BASE_URL}/search", json=payload)
    print("Search Response (With Category):", response.status_code)
    print(f"Found {response.json().get('result_count', 0)} activities")
    print(json.dumps(response.json(), indent=2)[:500] + "..." if len(json.dumps(response.json())) > 500 else json.dumps(response.json(), indent=2))
    print("\n---\n")
    
    # Test case 3: Search with price range
    payload = {
        "location": "New York",
        "datetime": "2025-04-19T14:00:00",
        "min_price": 0,
        "max_price": 50
    }
    response = requests.post(f"{BASE_URL}/search", json=payload)
    print("Search Response (With Price Range):", response.status_code)
    print(f"Found {response.json().get('result_count', 0)} activities")
    print(json.dumps(response.json(), indent=2)[:500] + "..." if len(json.dumps(response.json())) > 500 else json.dumps(response.json(), indent=2))
    print("\n---\n")
    
    # Test case 4: Search with all parameters
    payload = {
        "location": "New York",
        "datetime": "2025-04-19T14:00:00",
        "category": "indoor",
        "min_price": 20,
        "max_price": 100,
        "group_size": 4,
        "duration": 120  # in minutes
    }
    response = requests.post(f"{BASE_URL}/search", json=payload)
    print("Search Response (All Parameters):", response.status_code)
    print(f"Found {response.json().get('result_count', 0)} activities")
    print(json.dumps(response.json(), indent=2)[:500] + "..." if len(json.dumps(response.json())) > 500 else json.dumps(response.json(), indent=2))
    print("\n---\n")
    
    # Test case 5: Invalid location
    payload = {
        "location": "",
        "datetime": "2025-04-19T14:00:00"
    }
    response = requests.post(f"{BASE_URL}/search", json=payload)
    print("Search Response (Invalid Location):", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print("\n---\n")

def test_activity_details():
    """Test the activity details endpoint"""
    # First search for an activity to get an ID
    search_payload = {
        "location": "New York",
        "datetime": "2025-04-19T14:00:00"
    }
    search_response = requests.post(f"{BASE_URL}/search", json=search_payload)
    
    if search_response.status_code == 200 and search_response.json().get("results"):
        activity_id = search_response.json().get("results")[0].get("id")
        
        # Get activity details
        response = requests.get(f"{BASE_URL}/activity/{activity_id}")
        print(f"Activity Details Response (ID: {activity_id}):", response.status_code)
        print(json.dumps(response.json(), indent=2))
        print("\n---\n")
        
        # Test invalid ID
        invalid_id = "invalid_id_12345"
        response = requests.get(f"{BASE_URL}/activity/{invalid_id}")
        print(f"Activity Details Response (Invalid ID: {invalid_id}):", response.status_code)
        print(json.dumps(response.json(), indent=2))
        print("\n---\n")
    else:
        print("No activities found to test activity details endpoint.")
        print("\n---\n")

def test_booking():
    """Test the booking endpoint"""
    # First search for an activity to get an ID
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    search_payload = {
        "location": "New York",
        "datetime": tomorrow
    }
    search_response = requests.post(f"{BASE_URL}/search", json=search_payload)
    
    if search_response.status_code == 200 and search_response.json().get("results"):
        activity_id = search_response.json().get("results")[0].get("id")
        
        # Make a booking
        booking_payload = {
            "activity_id": activity_id,
            "user_id": "test_user_123",
            "datetime": tomorrow,
            "group_size": 2,
            "contact_info": {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "123-456-7890"
            }
        }
        response = requests.post(f"{BASE_URL}/booking", json=booking_payload)
        print("Booking Response:", response.status_code)
        print(json.dumps(response.json(), indent=2))
        print("\n---\n")
        
        # Test invalid booking (past date)
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
        invalid_booking_payload = {
            "activity_id": activity_id,
            "user_id": "test_user_123",
            "datetime": past_date,
            "group_size": 2,
            "contact_info": {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "123-456-7890"
            }
        }
        response = requests.post(f"{BASE_URL}/booking", json=invalid_booking_payload)
        print("Invalid Booking Response (Past Date):", response.status_code)
        print(json.dumps(response.json(), indent=2))
        print("\n---\n")
    else:
        print("No activities found to test booking endpoint.")
        print("\n---\n")

def test_user_bookings():
    """Test the user bookings endpoint"""
    user_id = "test_user_123"
    response = requests.get(f"{BASE_URL}/user/{user_id}/bookings")
    print(f"User Bookings Response (User ID: {user_id}):", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print("\n---\n")
    
    # Test invalid user ID
    invalid_user_id = "nonexistent_user"
    response = requests.get(f"{BASE_URL}/user/{invalid_user_id}/bookings")
    print(f"User Bookings Response (Invalid User ID: {invalid_user_id}):", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print("\n---\n")

def run_all_tests():
    """Run all test functions"""
    print("=== STARTING API TESTS ===\n")
    
    # Run all test functions
    test_health_check()
    test_categories()
    test_search()
    test_activity_details()
    test_booking()
    test_user_bookings()
    
    print("=== API TESTS COMPLETED ===\n")

if __name__ == "__main__":
    run_all_tests()