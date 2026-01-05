# Analytics API Documentation

## Overview
The Analytics app provides comprehensive metrics, statistics, and reporting capabilities for the Service Marketplace Platform. All endpoints require Admin authentication.

## API Endpoints

### 1. Dashboard Metrics
**GET** `/api/analytics/dashboard/`

Returns real-time platform metrics.

**Query Parameters:**
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)

**Response:**
```json
{
  "total_users": 150,
  "total_regular_users": 100,
  "total_providers": 45,
  "active_providers": 40,
  "pending_applications": 5,
  "pending_requests": 20,
  "accepted_requests": 50,
  "completed_requests": 30,
  "rejected_requests": 10,
  "total_services": 75
}
```

### 2. User Registration Statistics
**GET** `/api/analytics/users/registrations/`

Returns daily user registration counts over time.

**Query Parameters:**
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `role` (optional): Filter by role (REGULAR, PROVIDER, ADMIN)

**Response:**
```json
[
  {
    "date": "2024-01-01",
    "count": 5
  },
  {
    "date": "2024-01-02",
    "count": 8
  }
]
```

### 3. Service Request Statistics
**GET** `/api/analytics/requests/stats/`

Returns daily service request counts over time.

**Query Parameters:**
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `status` (optional): Filter by status (PENDING, ACCEPTED, REJECTED, COMPLETED)

**Response:**
```json
[
  {
    "date": "2024-01-01",
    "count": 12
  },
  {
    "date": "2024-01-02",
    "count": 15
  }
]
```

### 4. Provider Activity Statistics
**GET** `/api/analytics/providers/activity/`

Returns provider activity metrics including services and requests.

**Query Parameters:**
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "email": "provider@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T10:00:00Z",
    "services_count": 5,
    "received_requests_count": 20,
    "accepted_requests_count": 15,
    "completed_requests_count": 10
  }
]
```

### 5. User Search
**GET** `/api/analytics/users/search/`

Search users by email or name with pagination.

**Query Parameters:**
- `q` (optional): Search query
- `role` (optional): Filter by role (REGULAR, PROVIDER, ADMIN)

**Response:**
```json
{
  "count": 100,
  "next": "http://api/analytics/users/search/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "full_name": "Jane Smith",
      "role": "REGULAR",
      "is_active": true,
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

### 6. Provider Search
**GET** `/api/analytics/providers/search/`

Search providers by email, name, or service description with pagination.

**Query Parameters:**
- `q` (optional): Search query

**Response:**
```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "provider@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "service_description": "Professional plumbing services",
      "approval_status": "APPROVED",
      "created_at": "2024-01-01T10:00:00Z",
      "approved_at": "2024-01-02T10:00:00Z"
    }
  ]
}
```

### 7. Request Search
**GET** `/api/analytics/requests/search/`

Search service requests by service name or user details with pagination.

**Query Parameters:**
- `q` (optional): Search query
- `status` (optional): Filter by status (PENDING, ACCEPTED, REJECTED, COMPLETED)

**Response:**
```json
{
  "count": 75,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "service_name": "Plumbing Repair",
      "requester_email": "user@example.com",
      "requester_name": "Jane Smith",
      "provider_email": "provider@example.com",
      "provider_name": "John Doe",
      "status": "ACCEPTED",
      "message": "Need urgent repair",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T11:00:00Z"
    }
  ]
}
```

### 8. CSV Export
**GET** `/api/analytics/export/`

Export analytics data as CSV file.

**Query Parameters:**
- `type` (required): Export type (users, providers, requests, metrics)
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `role` (optional, for users): Filter by role (REGULAR, PROVIDER, ADMIN)
- `status` (optional, for requests): Filter by status (PENDING, ACCEPTED, REJECTED, COMPLETED)

**Response:**
Returns a CSV file with appropriate headers and data.

**Examples:**
- Export all users: `/api/analytics/export/?type=users`
- Export providers: `/api/analytics/export/?type=providers&start_date=2024-01-01`
- Export pending requests: `/api/analytics/export/?type=requests&status=PENDING`
- Export metrics: `/api/analytics/export/?type=metrics`

## Authentication
All endpoints require:
- Valid JWT token in Authorization header
- User role must be ADMIN

**Example:**
```
Authorization: Bearer <jwt_token>
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid role. Must be REGULAR, PROVIDER, or ADMIN."
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```
