import requests
import json

# First, get JWT token
login_url = "http://localhost:8000/api/auth/login/"
login_data = {
    "email": "admin@marketplace.com",
    "password": "admin123"
}

login_response = requests.post(login_url, json=login_data)
print(f"Login Status: {login_response.status_code}")

if login_response.status_code != 200:
    print("Login failed!")
    print(login_response.text)
    exit(1)

login_data_response = login_response.json()
print(f"Login response: {json.dumps(login_data_response, indent=2)}")

token = login_data_response.get('tokens', {}).get('access')
print(f"Got token: {token[:20]}...")

# Test the provider applications endpoint
url = "http://localhost:8000/api/auth/providers/applications/"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"\nResponse JSON:")
print(json.dumps(response.json(), indent=2))

# Check if user_details field exists
if response.status_code == 200:
    data = response.json()
    if data.get('results'):
        first_app = data['results'][0]
        print(f"\n✓ First application has 'user_details': {'user_details' in first_app}")
        print(f"✓ First application has 'user' field: {'user' in first_app}")
        if 'user_details' in first_app:
            print(f"✓ user_details contains: {list(first_app['user_details'].keys())}")
