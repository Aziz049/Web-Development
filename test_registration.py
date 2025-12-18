"""
Test script for patient registration
Run this to test the registration endpoint
"""
import requests
import json

# Test data
test_data = {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "gender": "M",
    "username": "testuser123",
    "email": "test@example.com",
    "phone_number": "+96512345678",
    "password": "TestPass123",
    "password2": "TestPass123",
    "consent_treatment": True
}

# Test endpoint
url = "http://localhost:8000/api/register/patient/"

try:
    response = requests.post(
        url,
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
    else:
        print("❌ Registration failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")


