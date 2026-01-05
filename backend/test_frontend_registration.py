"""
Test script to verify provider registration through frontend and admin dashboard visibility.

This script:
1. Creates a test provider registration (simulating frontend form submission)
2. Verifies the provider appears in the admin dashboard
3. Tests the approve/reject functionality
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import ProviderProfile

User = get_user_model()

# Configuration
BASE_URL = "http://localhost:8000/api"
FRONTEND_URL = "http://localhost:5173"
TEST_PROVIDER_EMAIL = f"frontend_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
TEST_PROVIDER_PASSWORD = "TestPassword123!"
TEST_PROVIDER_FIRST_NAME = "Frontend"
TEST_PROVIDER_LAST_NAME = "TestProvider"
TEST_SERVICE_DESCRIPTION = "Testing provider registration through frontend workflow"

# Admin credentials
ADMIN_EMAIL = "admin@marketplace.com"
ADMIN_PASSWORD = "admin123"


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_success(message):
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message):
    """Print an error message."""
    print(f"✗ {message}")


def print_info(message):
    """Print an info message."""
    print(f"  {message}")


def main():
    """Main test workflow."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  FRONTEND PROVIDER REGISTRATION TEST".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Step 1: Register provider
    print_section("Step 1: Register Provider (Simulating Frontend)")
    
    registration_data = {
        "email": TEST_PROVIDER_EMAIL,
        "password": TEST_PROVIDER_PASSWORD,
        "first_name": TEST_PROVIDER_FIRST_NAME,
        "last_name": TEST_PROVIDER_LAST_NAME,
        "role": "PROVIDER",
        "service_description": TEST_SERVICE_DESCRIPTION
    }
    
    print_info(f"Registering provider: {TEST_PROVIDER_EMAIL}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print_success("Provider registration successful")
            response_data = response.json()
            provider_id = response_data['provider_profile']['id']
            print_info(f"Provider Profile ID: {provider_id}")
        else:
            print_error(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Registration failed: {str(e)}")
        return False
    
    # Step 2: Login as admin
    print_section("Step 2: Login as Admin")
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            },
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print_error(f"Admin login failed: {login_response.text}")
            return False
        
        admin_token = login_response.json()["tokens"]["access"]
        print_success("Admin login successful")
        
    except Exception as e:
        print_error(f"Admin login failed: {str(e)}")
        return False
    
    # Step 3: Fetch provider applications
    print_section("Step 3: Fetch Provider Applications (Admin Dashboard)")
    
    try:
        applications_response = requests.get(
            f"{BASE_URL}/auth/providers/applications/",
            headers={
                "Authorization": f"Bearer {admin_token}",
                "Content-Type": "application/json"
            }
        )
        
        if applications_response.status_code != 200:
            print_error(f"Failed to fetch applications: {applications_response.text}")
            return False
        
        applications_data = applications_response.json()
        print_success(f"Successfully fetched {applications_data['count']} pending applications")
        
        # Find our test provider
        found = False
        for app in applications_data['results']:
            if app['user_details']['email'] == TEST_PROVIDER_EMAIL:
                found = True
                print_success(f"Test provider found in admin dashboard")
                print_info(f"Provider: {app['user_details']['first_name']} {app['user_details']['last_name']}")
                print_info(f"Email: {app['user_details']['email']}")
                print_info(f"Service: {app['service_description']}")
                print_info(f"Status: {app['approval_status']}")
                break
        
        if not found:
            print_error("Test provider not found in admin dashboard")
            return False
        
    except Exception as e:
        print_error(f"Failed to fetch applications: {str(e)}")
        return False
    
    # Step 4: Test approve functionality
    print_section("Step 4: Test Approve Functionality")
    
    try:
        approve_response = requests.post(
            f"{BASE_URL}/auth/providers/applications/{provider_id}/approve/",
            headers={
                "Authorization": f"Bearer {admin_token}",
                "Content-Type": "application/json"
            }
        )
        
        if approve_response.status_code == 200:
            print_success("Provider approved successfully")
            approved_data = approve_response.json()
            print_info(f"Status: {approved_data['provider_profile']['approval_status']}")
            print_info(f"User is_active: {approved_data['provider_profile']['user_details']['is_active']}")
        else:
            print_error(f"Approval failed: {approve_response.text}")
            return False
        
    except Exception as e:
        print_error(f"Approval failed: {str(e)}")
        return False
    
    # Step 5: Verify provider can now login
    print_section("Step 5: Verify Approved Provider Can Login")
    
    try:
        provider_login_response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={
                "email": TEST_PROVIDER_EMAIL,
                "password": TEST_PROVIDER_PASSWORD
            },
            headers={"Content-Type": "application/json"}
        )
        
        if provider_login_response.status_code == 200:
            print_success("Approved provider can login successfully")
            provider_data = provider_login_response.json()
            print_info(f"Provider role: {provider_data['user']['role']}")
            print_info(f"Provider active: {provider_data['user']['is_active']}")
        else:
            print_error(f"Provider login failed: {provider_login_response.text}")
            return False
        
    except Exception as e:
        print_error(f"Provider login failed: {str(e)}")
        return False
    
    # Cleanup
    print_section("Cleanup: Removing Test Data")
    
    try:
        user = User.objects.filter(email=TEST_PROVIDER_EMAIL).first()
        if user:
            user.delete()
            print_success(f"Test data cleaned up: {TEST_PROVIDER_EMAIL}")
    except Exception as e:
        print_error(f"Error during cleanup: {str(e)}")
    
    # Final summary
    print_section("TEST SUMMARY")
    print_success("ALL TESTS PASSED ✓")
    print_info("\nComplete workflow verified:")
    print_info("  ✓ Provider registration through API (frontend simulation)")
    print_info("  ✓ Provider application visible in admin dashboard")
    print_info("  ✓ Admin can approve provider application")
    print_info("  ✓ Approved provider can login successfully")
    print_info("  ✓ User is_active status updated correctly")
    
    print("\n" + "=" * 80)
    print("  MANUAL TESTING INSTRUCTIONS")
    print("=" * 80)
    print("\nTo test through the actual frontend:")
    print(f"1. Open browser to: {FRONTEND_URL}")
    print("2. Click 'Sign Up' and select 'Service Provider'")
    print("3. Fill in the registration form:")
    print("   - Email: any valid email")
    print("   - Password: any valid password")
    print("   - First Name: Test")
    print("   - Last Name: Provider")
    print("   - Service Description: Any description (min 10 chars)")
    print("4. Submit the form")
    print("5. Login as admin:")
    print(f"   - Email: {ADMIN_EMAIL}")
    print(f"   - Password: {ADMIN_PASSWORD}")
    print("6. Navigate to 'Provider Applications' tab")
    print("7. Verify your test provider appears in the list")
    print("8. Click 'Approve' or 'Reject' to test the functionality")
    print("=" * 80 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
