import requests
import json

# Login as admin
login_url = "http://localhost:8000/api/auth/login/"
login_data = {
    "email": "admin@marketplace.com",
    "password": "admin123"
}

login_response = requests.post(login_url, json=login_data)
token = login_response.json().get('tokens', {}).get('access')

headers = {
    "Authorization": f"Bearer {token}"
}

# Get pending applications
print("=" * 60)
print("PENDING PROVIDER APPLICATIONS")
print("=" * 60)

url = "http://localhost:8000/api/auth/providers/applications/"
response = requests.get(url, headers=headers)
data = response.json()

print(f"\nTotal pending applications: {data['count']}\n")

for i, app in enumerate(data['results'], 1):
    print(f"{i}. {app['user_details']['first_name']} {app['user_details']['last_name']}")
    print(f"   Email: {app['user_details']['email']}")
    print(f"   Service: {app['service_description'][:50]}...")
    print(f"   Application ID: {app['id']}")
    print()

# Test approve endpoint (without actually approving)
if data['results']:
    first_app_id = data['results'][0]['id']
    print(f"\nTest: Checking approve endpoint for application ID {first_app_id}")
    approve_url = f"http://localhost:8000/api/auth/providers/applications/{first_app_id}/approve/"
    print(f"Approve URL: {approve_url}")
    
    print(f"\nTest: Checking reject endpoint for application ID {first_app_id}")
    reject_url = f"http://localhost:8000/api/auth/providers/applications/{first_app_id}/reject/"
    print(f"Reject URL: {reject_url}")

print("\n" + "=" * 60)
print("Ready for manual testing in the browser!")
print("=" * 60)
print(f"\nFrontend URL: http://localhost:5174/")
print(f"Admin Login: admin@marketplace.com / admin123")
print("\nNavigate to the Provider Applications tab to test the UI.")
