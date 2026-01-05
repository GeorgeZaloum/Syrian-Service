"""
Verification script for provider registration workflow.

This script tests the complete provider registration workflow:
1. Register a new service provider through the API
2. Verify User record is created with role='PROVIDER' and is_active=False
3. Verify ProviderProfile record is created with approval_status='PENDING'
4. Verify the ProviderProfile is linked to the User via foreign key
5. Verify the service_description is stored correctly
6. Verify the application appears in the admin API endpoint
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
TEST_PROVIDER_EMAIL = f"test_provider_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
TEST_PROVIDER_PASSWORD = "TestPassword123!"
TEST_PROVIDER_FIRST_NAME = "Test"
TEST_PROVIDER_LAST_NAME = "Provider"
TEST_SERVICE_DESCRIPTION = "Professional testing services for software applications"

# Admin credentials (from sample data)
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


def register_provider_via_api():
    """Register a new provider through the API."""
    print_section("Step 1: Register Provider via API")
    
    registration_data = {
        "email": TEST_PROVIDER_EMAIL,
        "password": TEST_PROVIDER_PASSWORD,
        "first_name": TEST_PROVIDER_FIRST_NAME,
        "last_name": TEST_PROVIDER_LAST_NAME,
        "role": "PROVIDER",
        "service_description": TEST_SERVICE_DESCRIPTION
    }
    
    print_info(f"Registering provider: {TEST_PROVIDER_EMAIL}")
    print_info(f"Service description: {TEST_SERVICE_DESCRIPTION}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Response status: {response.status_code}")
        
        if response.status_code == 201:
            response_data = response.json()
            print_success("Provider registration successful")
            print_info(f"Response: {json.dumps(response_data, indent=2)}")
            return True, response_data
        else:
            print_error(f"Registration failed: {response.text}")
            return False, None
            
    except Exception as e:
        print_error(f"API request failed: {str(e)}")
        return False, None


def verify_user_record():
    """Verify the User record was created correctly."""
    print_section("Step 2: Verify User Record in Database")
    
    try:
        user = User.objects.get(email=TEST_PROVIDER_EMAIL)
        print_success(f"User record found: ID={user.id}")
        
        # Verify role
        if user.role == 'PROVIDER':
            print_success(f"User role is correct: {user.role}")
        else:
            print_error(f"User role is incorrect: {user.role} (expected: PROVIDER)")
            return False, None
        
        # Verify is_active
        if user.is_active == False:
            print_success(f"User is_active is correct: {user.is_active} (inactive until approved)")
        else:
            print_error(f"User is_active is incorrect: {user.is_active} (expected: False)")
            return False, None
        
        # Verify name
        if user.first_name == TEST_PROVIDER_FIRST_NAME and user.last_name == TEST_PROVIDER_LAST_NAME:
            print_success(f"User name is correct: {user.full_name}")
        else:
            print_error(f"User name is incorrect: {user.full_name}")
            return False, None
        
        print_info(f"User details:")
        print_info(f"  - ID: {user.id}")
        print_info(f"  - Email: {user.email}")
        print_info(f"  - Name: {user.full_name}")
        print_info(f"  - Role: {user.role}")
        print_info(f"  - Active: {user.is_active}")
        print_info(f"  - Created: {user.created_at}")
        
        return True, user
        
    except User.DoesNotExist:
        print_error(f"User record not found for email: {TEST_PROVIDER_EMAIL}")
        return False, None
    except Exception as e:
        print_error(f"Error verifying user record: {str(e)}")
        return False, None


def verify_provider_profile(user):
    """Verify the ProviderProfile record was created correctly."""
    print_section("Step 3: Verify ProviderProfile Record in Database")
    
    try:
        provider_profile = ProviderProfile.objects.get(user=user)
        print_success(f"ProviderProfile record found: ID={provider_profile.id}")
        
        # Verify approval_status
        if provider_profile.approval_status == 'PENDING':
            print_success(f"Approval status is correct: {provider_profile.approval_status}")
        else:
            print_error(f"Approval status is incorrect: {provider_profile.approval_status} (expected: PENDING)")
            return False, None
        
        # Verify service_description
        if provider_profile.service_description == TEST_SERVICE_DESCRIPTION:
            print_success(f"Service description is correct")
        else:
            print_error(f"Service description is incorrect")
            return False, None
        
        # Verify foreign key relationship
        if provider_profile.user.id == user.id:
            print_success(f"ProviderProfile is correctly linked to User via foreign key")
        else:
            print_error(f"ProviderProfile foreign key relationship is incorrect")
            return False, None
        
        print_info(f"ProviderProfile details:")
        print_info(f"  - ID: {provider_profile.id}")
        print_info(f"  - User ID: {provider_profile.user.id}")
        print_info(f"  - User Email: {provider_profile.user.email}")
        print_info(f"  - Service Description: {provider_profile.service_description}")
        print_info(f"  - Approval Status: {provider_profile.approval_status}")
        print_info(f"  - Approved By: {provider_profile.approved_by}")
        print_info(f"  - Created: {provider_profile.created_at}")
        
        return True, provider_profile
        
    except ProviderProfile.DoesNotExist:
        print_error(f"ProviderProfile record not found for user: {user.email}")
        return False, None
    except Exception as e:
        print_error(f"Error verifying provider profile: {str(e)}")
        return False, None


def verify_admin_api_visibility():
    """Verify the application appears in the admin API endpoint."""
    print_section("Step 4: Verify Application Appears in Admin API")
    
    # First, login as admin to get access token
    print_info("Logging in as admin...")
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
    
    # Now fetch provider applications
    print_info("Fetching provider applications...")
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
        print_success(f"Successfully fetched applications")
        print_info(f"Total pending applications: {applications_data['count']}")
        
        # Check if our test provider is in the list
        found = False
        for app in applications_data['results']:
            if app['user_details']['email'] == TEST_PROVIDER_EMAIL:
                found = True
                print_success(f"Test provider application found in admin API")
                print_info(f"Application details:")
                print_info(f"  - ID: {app['id']}")
                print_info(f"  - Provider Name: {app['user_details']['first_name']} {app['user_details']['last_name']}")
                print_info(f"  - Provider Email: {app['user_details']['email']}")
                print_info(f"  - Service Description: {app['service_description']}")
                print_info(f"  - Approval Status: {app['approval_status']}")
                print_info(f"  - Created: {app['created_at']}")
                
                # Verify the response structure matches frontend expectations
                if 'user_details' in app:
                    print_success("Response contains 'user_details' field (matches frontend expectations)")
                else:
                    print_error("Response missing 'user_details' field")
                    return False
                
                if 'user' not in app:
                    print_success("Response does not contain deprecated 'user' field")
                else:
                    print_error("Response contains deprecated 'user' field")
                
                break
        
        if not found:
            print_error(f"Test provider application not found in admin API")
            print_info(f"Available applications:")
            for app in applications_data['results']:
                print_info(f"  - {app['user_details']['email']}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Failed to fetch applications: {str(e)}")
        return False


def cleanup_test_data():
    """Clean up test data created during verification."""
    print_section("Cleanup: Removing Test Data")
    
    try:
        user = User.objects.filter(email=TEST_PROVIDER_EMAIL).first()
        if user:
            # ProviderProfile will be deleted automatically due to CASCADE
            user.delete()
            print_success(f"Test data cleaned up: {TEST_PROVIDER_EMAIL}")
        else:
            print_info("No test data to clean up")
    except Exception as e:
        print_error(f"Error during cleanup: {str(e)}")


def main():
    """Main verification workflow."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  PROVIDER REGISTRATION WORKFLOW VERIFICATION".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    all_passed = True
    
    # Step 1: Register provider via API
    success, response_data = register_provider_via_api()
    if not success:
        print_error("Provider registration failed. Aborting verification.")
        return False
    
    # Step 2: Verify User record
    success, user = verify_user_record()
    if not success:
        all_passed = False
    
    # Step 3: Verify ProviderProfile record
    if user:
        success, provider_profile = verify_provider_profile(user)
        if not success:
            all_passed = False
    else:
        print_error("Skipping ProviderProfile verification (User not found)")
        all_passed = False
    
    # Step 4: Verify admin API visibility
    success = verify_admin_api_visibility()
    if not success:
        all_passed = False
    
    # Cleanup
    cleanup_test_data()
    
    # Final summary
    print_section("VERIFICATION SUMMARY")
    if all_passed:
        print_success("ALL VERIFICATIONS PASSED ✓")
        print_info("\nThe provider registration workflow is working correctly:")
        print_info("  ✓ User record created with role='PROVIDER' and is_active=False")
        print_info("  ✓ ProviderProfile record created with approval_status='PENDING'")
        print_info("  ✓ ProviderProfile correctly linked to User via foreign key")
        print_info("  ✓ Service description stored correctly")
        print_info("  ✓ Application visible in admin dashboard API")
        return True
    else:
        print_error("SOME VERIFICATIONS FAILED ✗")
        print_info("\nPlease review the errors above and fix any issues.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
