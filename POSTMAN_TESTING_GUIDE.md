# Postman API Testing Guide

## Overview
This guide explains how to test the Service Marketplace Platform backend API using Postman.

## Files Included
- `Service_Marketplace_API.postman_collection.json` - Complete API collection with all endpoints
- `Service_Marketplace_API.postman_environment.json` - Environment variables for local testing

## Setup Instructions

### 1. Import Collection and Environment

1. Open Postman
2. Click **Import** button (top left)
3. Drag and drop both JSON files or click **Upload Files**
4. Select both files:
   - `Service_Marketplace_API.postman_collection.json`
   - `Service_Marketplace_API.postman_environment.json`
5. Click **Import**

### 2. Select Environment

1. In the top-right corner, click the environment dropdown
2. Select **Service Marketplace - Local**
3. Verify the `base_url` is set to `http://localhost:8000/api`

### 3. Start Backend Server

Make sure your Django backend is running:

```bash
cd backend
python manage.py runserver
```

## Testing Workflow

### Step 1: Register Users

#### Register a Regular User
1. Navigate to **Authentication** → **Register Regular User**
2. Click **Send**
3. The response will contain the user details
4. The `user_id` is automatically saved to environment variables

#### Register a Service Provider
1. Navigate to **Authentication** → **Register Service Provider**
2. Click **Send**
3. The provider account is created with `PENDING` approval status
4. The `user_id` and `provider_profile_id` are automatically saved

### Step 2: Login

1. Navigate to **Authentication** → **Login**
2. Update the email/password in the request body to match your registered user
3. Click **Send**
4. The `access_token` and `refresh_token` are automatically saved to environment variables
5. All subsequent requests will use this token automatically

**Example Login Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```

### Step 3: Test User Endpoints

#### Get Current User Profile
1. Navigate to **Authentication** → **Get Current User**
2. Click **Send**
3. You should see your user profile information

#### Change Password
1. Navigate to **Authentication** → **Change Password**
2. Update the passwords in the request body
3. Click **Send**

### Step 4: Test Provider Approval (Admin Only)

To test admin endpoints, you need to:
1. Create an admin user via Django shell or admin panel
2. Login as admin to get admin access token

#### Create Admin User (via Django shell):
```bash
cd backend
python manage.py shell
```

```python
from apps.users.models import User
admin = User.objects.create_superuser(
    email='admin@example.com',
    password='AdminPass123!',
    first_name='Admin',
    last_name='User'
)
```

#### Approve Provider Application
1. Login as admin
2. Navigate to **Provider Management (Admin)** → **List Provider Applications**
3. Copy a `provider_profile_id` from the response
4. Update the `provider_profile_id` environment variable
5. Navigate to **Approve Provider**
6. Click **Send**

### Step 5: Test Services

#### Create a Service (Provider Only)
1. Login as an approved provider
2. Navigate to **Services** → **Create Service**
3. Update the service details in the request body
4. Click **Send**
5. The `service_id` is automatically saved

**Example Service Body:**
```json
{
    "name": "Professional Plumbing Services",
    "description": "Expert plumbing repairs, installations, and maintenance.",
    "location": "New York, NY",
    "cost": 150.00
}
```

#### List Services
1. Navigate to **Services** → **List Services**
2. Optionally add query parameters for filtering
3. Click **Send**
4. This endpoint doesn't require authentication

#### Get Service Detail
1. Navigate to **Services** → **Get Service Detail**
2. Make sure `service_id` is set in environment variables
3. Click **Send**

#### Update Service
1. Navigate to **Services** → **Update Service**
2. Modify the service details
3. Click **Send**

#### Get My Services
1. Login as a provider
2. Navigate to **Services** → **Get My Services**
3. Click **Send**

### Step 6: Test Service Requests

#### Create Service Request (Regular User Only)
1. Login as a regular user
2. Navigate to **Service Requests** → **Create Service Request**
3. Make sure `service_id` is set in environment variables
4. Update the message
5. Click **Send**
6. The `request_id` is automatically saved

**Example Request Body:**
```json
{
    "service": 1,
    "message": "I need plumbing services for a leaking pipe."
}
```

#### List Service Requests
1. Navigate to **Service Requests** → **List Service Requests**
2. Click **Send**
3. Regular users see their sent requests
4. Providers see requests for their services

#### Accept/Reject Request (Provider Only)
1. Login as the provider who owns the service
2. Navigate to **Service Requests** → **Accept Service Request**
3. Make sure `request_id` is set
4. Click **Send**

### Step 7: Test Problem Reports

#### Submit Problem Report (Text)
1. Login as any user
2. Navigate to **Problem Reports** → **Create Problem Report (Text)**
3. Update the problem description
4. Click **Send**
5. The response includes AI-generated recommendations
6. The `problem_id` is automatically saved

**Example Problem Body:**
```json
{
    "input_type": "TEXT",
    "problem_text": "My kitchen sink is leaking and water is pooling under the cabinet."
}
```

#### Submit Problem Report (Voice)
1. Navigate to **Problem Reports** → **Create Problem Report (Voice)**
2. In the Body tab, select the `audio_file` field
3. Click **Select Files** and choose an audio file
4. Click **Send**
5. The audio is transcribed and AI recommendations are generated

#### List Problem Reports
1. Navigate to **Problem Reports** → **List Problem Reports**
2. Click **Send**
3. You'll see all your submitted problem reports

#### Get Problem Detail
1. Navigate to **Problem Reports** → **Get Problem Report Detail**
2. Make sure `problem_id` is set
3. Click **Send**

### Step 8: Test Analytics (Admin Only)

#### Dashboard Metrics
1. Login as admin
2. Navigate to **Analytics (Admin)** → **Dashboard Metrics**
3. Click **Send**
4. You'll see overall platform statistics

#### User Registration Stats
1. Navigate to **Analytics (Admin)** → **User Registration Stats**
2. Update the date range in query parameters
3. Click **Send**

#### Export Data
1. Navigate to **Analytics (Admin)** → **Export Data to CSV**
2. Update the `data_type` parameter (users, providers, requests, services)
3. Click **Send**
4. The response will be a CSV file

## Environment Variables

The collection uses these environment variables (automatically managed):

| Variable | Description | Auto-Set |
|----------|-------------|----------|
| `base_url` | API base URL | Manual |
| `access_token` | JWT access token | Yes (on login) |
| `refresh_token` | JWT refresh token | Yes (on login) |
| `user_id` | Current user ID | Yes (on register) |
| `service_id` | Last created service ID | Yes (on create) |
| `request_id` | Last created request ID | Yes (on create) |
| `problem_id` | Last created problem ID | Yes (on create) |
| `provider_profile_id` | Provider profile ID | Yes (on register) |

## Authentication

Most endpoints require authentication. The collection is configured to automatically use the `access_token` from environment variables.

### Token Refresh
When your access token expires:
1. Navigate to **Authentication** → **Refresh Token**
2. Click **Send**
3. A new `access_token` is automatically saved

## Query Parameters

Many endpoints support filtering via query parameters:

### Services
- `search` - Search by name or description
- `location` - Filter by location
- `min_cost` - Minimum cost
- `max_cost` - Maximum cost

### Service Requests
- `status` - Filter by status (PENDING, ACCEPTED, REJECTED, COMPLETED)

### Analytics
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD)
- `role` - Filter by user role
- `approval_status` - Filter by approval status

## Common Issues

### 401 Unauthorized
- Your access token has expired
- Use the **Refresh Token** endpoint
- Or login again

### 403 Forbidden
- You don't have permission for this endpoint
- Check if you're using the correct user role
- Admin endpoints require admin user
- Provider endpoints require approved provider

### 404 Not Found
- The resource doesn't exist
- Check the ID in environment variables
- Make sure you created the resource first

### 400 Bad Request
- Invalid data in request body
- Check the error message in response
- Verify required fields are present

## Testing Different User Roles

### Regular User Can:
- Register and login
- Search and view services
- Create service requests
- Submit problem reports
- View their own requests and problems

### Service Provider Can:
- All regular user actions
- Create, update, delete their services
- View requests for their services
- Accept/reject service requests

### Admin Can:
- All actions
- Approve/reject provider applications
- View all analytics
- Search all users, providers, requests
- Export data to CSV

## Tips

1. **Use Test Scripts**: The collection includes test scripts that automatically save IDs to environment variables
2. **Check Response**: Always check the response to verify the request was successful
3. **Sequential Testing**: Follow the workflow order for best results
4. **Environment Variables**: Use `{{variable_name}}` syntax to reference variables in requests
5. **Save Requests**: Save modified requests to your collection for reuse

## Sample Test Scenario

Here's a complete test scenario:

1. Register a regular user
2. Register a service provider
3. Create admin user (via Django shell)
4. Login as admin
5. Approve the provider
6. Login as provider
7. Create a service
8. Login as regular user
9. Create a service request
10. Login as provider
11. Accept the service request
12. Login as regular user
13. Submit a problem report
14. Login as admin
15. View analytics dashboard

## Support

For issues or questions:
- Check the Django backend logs
- Verify the backend server is running
- Check environment variable values
- Review the API response error messages
