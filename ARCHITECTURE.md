# Service Marketplace Platform - Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Technology Stack](#technology-stack)
4. [Directory Structure](#directory-structure)
5. [Design Patterns and SOLID Principles](#design-patterns-and-solid-principles)
6. [API Endpoints](#api-endpoints)
7. [Database Schema](#database-schema)
8. [Authentication and Authorization](#authentication-and-authorization)
9. [Key Components](#key-components)

## System Overview

The Service Marketplace Platform is a full-stack web application that connects regular users seeking services with service providers. The system supports three user roles:

- **Regular Users**: Search for services, submit service requests, and report problems with AI-powered recommendations
- **Service Providers**: Manage services, respond to service requests, and track business activity
- **Admins**: Approve provider applications, view analytics, and export reports

### Core Features
- Role-based authentication with JWT tokens
- Service search and filtering by location and cost
- Service request workflow with email notifications
- Problem reporting with AI recommendations (text and voice input)
- Provider approval workflow
- Admin analytics dashboard with CSV export
- Animated landing page with modern UI

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  ┌────────────┐  ┌──────────┐  ┌─────────────────────────┐ │
│  │   Pages    │  │Components│  │  State Management       │ │
│  │            │  │          │  │  (Context API)          │ │
│  └────────────┘  └──────────┘  └─────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           API Client (Axios + React Query)              ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (Django + DRF)                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              API Layer (Views)                          ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │         Business Logic Layer (Services)                 ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │      Data Access Layer (Models + Repositories)          ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   PostgreSQL DB  │
                    └──────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL 15+
- **Authentication**: JWT (djangorestframework-simplejwt)
- **AI/ML**: OpenAI API for problem recommendations
- **Email**: Django email backend with SMTP
- **Testing**: pytest with pytest-django

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **UI Components**: Radix UI primitives, shadcn/ui
- **Styling**: TailwindCSS
- **Animations**: Framer Motion
- **State Management**: React Context API, React Query
- **HTTP Client**: Axios
- **Testing**: Vitest, React Testing Library

### Development Tools
- **Version Control**: Git
- **API Testing**: Postman
- **Code Quality**: ESLint, Prettier (frontend), Black, isort (backend)

## Directory Structure

### Backend Structure
```
backend/
├── config/                    # Django project configuration
│   ├── settings/
│   │   ├── base.py           # Base settings
│   │   ├── development.py    # Development settings
│   │   └── production.py     # Production settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI application
├── apps/
│   ├── users/                # User management app
│   │   ├── models.py         # User and ProviderProfile models
│   │   ├── serializers.py    # User serializers
│   │   ├── views.py          # Authentication and user views
│   │   ├── services.py       # Business logic services
│   │   ├── repositories.py   # Data access layer
│   │   └── urls.py           # User app URLs
│   ├── services/             # Service management app
│   │   ├── models.py         # Service model
│   │   ├── serializers.py    # Service serializers
│   │   ├── views.py          # Service CRUD views
│   │   ├── services.py       # Service business logic
│   │   ├── repositories.py   # Service data access
│   │   └── urls.py           # Service app URLs
│   ├── requests/             # Service request app
│   │   ├── models.py         # ServiceRequest model
│   │   ├── serializers.py    # Request serializers
│   │   ├── views.py          # Request management views
│   │   ├── services.py       # Request workflow logic
│   │   ├── repositories.py   # Request data access
│   │   └── urls.py           # Request app URLs
│   ├── problems/             # Problem reporting app
│   │   ├── models.py         # ProblemReport model
│   │   ├── serializers.py    # Problem serializers
│   │   ├── views.py          # Problem reporting views
│   │   ├── services.py       # Problem processing logic
│   │   ├── ai_service.py     # AI recommendation service
│   │   └── urls.py           # Problem app URLs
│   └── analytics/            # Admin analytics app
│       ├── serializers.py    # Analytics serializers
│       ├── views.py          # Analytics and reporting views
│       ├── services.py       # Analytics aggregation logic
│       └── urls.py           # Analytics app URLs
├── core/                     # Shared utilities
│   ├── permissions.py        # Custom permission classes
│   ├── pagination.py         # Pagination utilities
│   ├── exceptions.py         # Custom exception classes
│   └── email_service.py      # Email notification service
├── media/                    # User-uploaded files
│   └── problem_audio/        # Voice recordings
├── templates/                # Email templates
│   └── emails/
├── tests/                    # Integration tests
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/               # shadcn/ui components (Button, Input, etc.)
│   │   ├── layout/           # Layout components (Header, Sidebar, Footer)
│   │   ├── auth/             # Authentication components
│   │   ├── landing/          # Landing page components
│   │   ├── user/             # Regular user dashboard components
│   │   ├── provider/         # Provider dashboard components
│   │   └── admin/            # Admin dashboard components
│   ├── pages/
│   │   ├── LandingPage.tsx   # Public landing page
│   │   ├── LoginPage.tsx     # Login page
│   │   ├── RegisterPage.tsx  # Registration page
│   │   ├── UserDashboard.tsx # Regular user dashboard
│   │   ├── ProviderDashboard.tsx # Provider dashboard
│   │   ├── AdminDashboard.tsx    # Admin dashboard
│   │   ├── NotFoundPage.tsx  # 404 error page
│   │   └── ErrorPage.tsx     # Generic error page
│   ├── lib/
│   │   ├── api/              # API client and endpoints
│   │   ├── store/            # State management
│   │   ├── utils.ts          # Utility functions
│   │   └── query-client.ts   # React Query configuration
│   ├── contexts/
│   │   └── AuthContext.tsx   # Authentication context
│   ├── hooks/
│   │   ├── use-toast.ts      # Toast notification hook
│   │   ├── useDebounce.ts    # Debounce hook
│   │   └── useIntersectionObserver.ts # Intersection observer hook
│   ├── routes/
│   │   └── index.tsx         # Route configuration
│   ├── types/                # TypeScript type definitions
│   │   ├── user.ts
│   │   ├── service.ts
│   │   ├── request.ts
│   │   ├── problem.ts
│   │   └── analytics.ts
│   ├── App.tsx               # Root component
│   └── main.tsx              # Application entry point
├── public/                   # Static assets
├── package.json              # Node dependencies
├── vite.config.ts            # Vite configuration
├── tailwind.config.js        # TailwindCSS configuration
└── tsconfig.json             # TypeScript configuration
```

## Design Patterns and SOLID Principles

### Design Patterns

#### 1. Repository Pattern
The backend uses the Repository pattern to abstract data access logic from business logic:

```python
# Example: ServiceRepository
class ServiceRepository:
    def get_all_active_services(self):
        return Service.objects.filter(is_active=True)
    
    def get_services_by_location(self, location):
        return Service.objects.filter(location__icontains=location, is_active=True)
    
    def get_services_by_cost_range(self, min_cost, max_cost):
        return Service.objects.filter(cost__gte=min_cost, cost__lte=max_cost, is_active=True)
```

**Benefits**:
- Separates data access from business logic
- Makes testing easier with mock repositories
- Centralizes query logic

#### 2. Service Layer Pattern
Business logic is encapsulated in service classes:

```python
# Example: ServiceRequestService
class ServiceRequestService:
    def __init__(self, repository, email_service):
        self.repository = repository
        self.email_service = email_service
    
    def create_request(self, service, requester, message):
        # Business logic for creating requests
        request = self.repository.create(...)
        self.email_service.send_request_notification(...)
        return request
```

**Benefits**:
- Keeps views thin and focused on HTTP concerns
- Reusable business logic
- Easier to test in isolation

#### 3. Factory Pattern
Used for creating complex objects like users with different roles:

```python
# Example: User registration with role-specific logic
def create_user_with_role(email, password, role, **kwargs):
    user = User.objects.create_user(email, password, role=role, **kwargs)
    if role == 'PROVIDER':
        ProviderProfile.objects.create(user=user, ...)
    return user
```

#### 4. Strategy Pattern
Used for handling different input types in problem reporting:

```python
# Example: Different strategies for text vs voice input
class TextInputStrategy:
    def process(self, input_data):
        return input_data['text']

class VoiceInputStrategy:
    def process(self, input_data):
        audio_file = input_data['audio']
        return transcribe_audio(audio_file)
```

### SOLID Principles

#### Single Responsibility Principle (SRP)
Each class has one reason to change:
- **Models**: Define data structure only
- **Serializers**: Handle data validation and transformation
- **Views**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Repositories**: Handle data access

#### Open/Closed Principle (OCP)
Classes are open for extension but closed for modification:
- Permission classes can be extended without modifying base classes
- Service classes can be extended with new functionality
- Serializers can be composed and extended

#### Liskov Substitution Principle (LSP)
Derived classes can substitute base classes:
- All user roles (Regular, Provider, Admin) use the same User model
- Different permission classes implement the same interface

#### Interface Segregation Principle (ISP)
Clients don't depend on interfaces they don't use:
- Role-specific serializers only include relevant fields
- API endpoints are separated by functionality
- Frontend components receive only the props they need

#### Dependency Inversion Principle (DIP)
High-level modules don't depend on low-level modules:
- Services depend on repository interfaces, not concrete implementations
- Views depend on service interfaces
- Email service is injected into services that need it

## API Endpoints

### Authentication & User Management (`/api/users/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/api/users/register/regular/` | Register as regular user | No | - |
| POST | `/api/users/register/provider/` | Register as service provider | No | - |
| POST | `/api/users/login/` | Login and get JWT tokens | No | - |
| POST | `/api/users/token/refresh/` | Refresh access token | No | - |
| GET | `/api/users/me/` | Get current user profile | Yes | All |
| POST | `/api/users/password/change/` | Change password | Yes | All |
| GET | `/api/users/providers/applications/` | List pending provider applications | Yes | Admin |
| POST | `/api/users/providers/applications/{id}/approve/` | Approve provider application | Yes | Admin |
| POST | `/api/users/providers/applications/{id}/reject/` | Reject provider application | Yes | Admin |

### Service Management (`/api/services/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/services/` | List/search services (with filters) | No | - |
| POST | `/api/services/` | Create new service | Yes | Provider |
| GET | `/api/services/{id}/` | Get service details | No | - |
| PUT | `/api/services/{id}/` | Update service | Yes | Provider (owner) |
| DELETE | `/api/services/{id}/` | Delete service | Yes | Provider (owner) |
| GET | `/api/services/my-services/` | Get provider's services | Yes | Provider |

**Query Parameters for GET `/api/services/`**:
- `location`: Filter by location (case-insensitive partial match)
- `min_cost`: Minimum cost filter
- `max_cost`: Maximum cost filter
- `search`: Search in name and description
- `page`: Page number for pagination
- `page_size`: Items per page (default: 10)

### Service Requests (`/api/requests/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/requests/` | List service requests (filtered by role) | Yes | User/Provider |
| POST | `/api/requests/` | Create service request | Yes | User |
| GET | `/api/requests/{id}/` | Get request details | Yes | User/Provider |
| POST | `/api/requests/{id}/accept/` | Accept service request | Yes | Provider |
| POST | `/api/requests/{id}/reject/` | Reject service request | Yes | Provider |

**Query Parameters for GET `/api/requests/`**:
- `status`: Filter by status (PENDING, ACCEPTED, REJECTED, COMPLETED)
- `page`: Page number for pagination

### Problem Reporting (`/api/problems/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/problems/` | List user's problem reports | Yes | User |
| POST | `/api/problems/create/` | Submit problem report | Yes | User |
| GET | `/api/problems/{id}/` | Get problem details with recommendations | Yes | User |

**POST `/api/problems/create/` Request Body**:
```json
{
  "input_type": "TEXT" | "VOICE",
  "problem_text": "string (required for TEXT)",
  "audio_file": "file (required for VOICE)"
}
```

### Analytics (`/api/analytics/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/analytics/dashboard/` | Get dashboard metrics | Yes | Admin |
| GET | `/api/analytics/users/registrations/` | User registration statistics | Yes | Admin |
| GET | `/api/analytics/requests/stats/` | Service request statistics | Yes | Admin |
| GET | `/api/analytics/providers/activity/` | Provider activity statistics | Yes | Admin |
| GET | `/api/analytics/users/search/` | Search users | Yes | Admin |
| GET | `/api/analytics/providers/search/` | Search providers | Yes | Admin |
| GET | `/api/analytics/requests/search/` | Search requests | Yes | Admin |
| GET | `/api/analytics/export/` | Export data as CSV | Yes | Admin |

**Query Parameters for Analytics Endpoints**:
- `start_date`: Filter from date (YYYY-MM-DD)
- `end_date`: Filter to date (YYYY-MM-DD)
- `role`: Filter by user role
- `status`: Filter by status
- `search`: Search query

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────────┐         ┌──────────────────────┐
│       User          │────────▶│  ProviderProfile     │
│                     │ 1     1 │                      │
│ PK: id              │         │ PK: id               │
│ UK: email           │         │ FK: user_id          │
│     first_name      │         │     service_desc     │
│     last_name       │         │     approval_status  │
│     role            │         │ FK: approved_by_id   │
│     is_active       │         │     approved_at      │
│     created_at      │         └──────────────────────┘
└─────────────────────┘
      │ 1
      │
      │ *
┌─────────────────────┐
│      Service        │
│                     │
│ PK: id              │
│ FK: provider_id     │────┐
│     name            │    │
│     description     │    │
│     location        │    │
│     cost            │    │
│     is_active       │    │
│     created_at      │    │
└─────────────────────┘    │
      │ 1                  │
      │                    │
      │ *                  │
┌─────────────────────┐    │
│  ServiceRequest     │    │
│                     │    │
│ PK: id              │    │
│ FK: service_id      │    │
│ FK: requester_id    │◀───┤
│ FK: provider_id     │────┘
│     status          │
│     message         │
│     created_at      │
└─────────────────────┘

┌─────────────────────┐
│   ProblemReport     │
│                     │
│ PK: id              │
│ FK: user_id         │────▶ User
│     input_type      │
│     problem_text    │
│     audio_file      │
│     recommendations │ (JSON)
│     created_at      │
└─────────────────────┘
```

### Table Schemas

#### users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (username) |
| password | VARCHAR(128) | NOT NULL | Hashed password |
| first_name | VARCHAR(100) | NOT NULL | User's first name |
| last_name | VARCHAR(100) | NOT NULL | User's last name |
| role | VARCHAR(10) | NOT NULL | REGULAR, PROVIDER, or ADMIN |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |
| is_staff | BOOLEAN | DEFAULT FALSE | Django admin access |
| created_at | TIMESTAMP | NOT NULL | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**: 
- `email` (unique)
- `created_at` (descending)

#### provider_profiles
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing ID |
| user_id | INTEGER | FOREIGN KEY, UNIQUE | Reference to users.id |
| service_description | TEXT | NOT NULL | Provider's service description |
| approval_status | VARCHAR(10) | NOT NULL | PENDING, APPROVED, or REJECTED |
| approved_by_id | INTEGER | FOREIGN KEY, NULL | Reference to admin user |
| approved_at | TIMESTAMP | NULL | Approval/rejection timestamp |
| created_at | TIMESTAMP | NOT NULL | Profile creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**:
- `user_id` (unique)
- `approval_status`
- `created_at` (descending)

#### services
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing ID |
| provider_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to users.id |
| name | VARCHAR(200) | NOT NULL | Service name |
| description | TEXT | NOT NULL | Service description |
| location | VARCHAR(200) | NOT NULL, INDEXED | Service location |
| cost | DECIMAL(10,2) | NOT NULL, INDEXED | Service cost |
| is_active | BOOLEAN | DEFAULT TRUE | Service active status |
| created_at | TIMESTAMP | NOT NULL | Service creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**:
- `provider_id, is_active` (composite)
- `location, cost` (composite)
- `created_at` (descending)

#### service_requests
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing ID |
| service_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to services.id |
| requester_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to users.id (requester) |
| provider_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to users.id (provider) |
| status | VARCHAR(20) | NOT NULL, INDEXED | PENDING, ACCEPTED, REJECTED, COMPLETED |
| message | TEXT | NULL | Optional message from requester |
| created_at | TIMESTAMP | NOT NULL, INDEXED | Request creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**:
- `requester_id, status` (composite)
- `provider_id, status` (composite)
- `service_id, status` (composite)
- `created_at` (descending)

#### problem_reports
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-incrementing ID |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to users.id |
| input_type | VARCHAR(10) | NOT NULL | TEXT or VOICE |
| problem_text | TEXT | NOT NULL | Problem description (or transcription) |
| audio_file | VARCHAR(100) | NULL | Path to audio file (if VOICE) |
| recommendations | JSON | NOT NULL | AI-generated recommendations array |
| created_at | TIMESTAMP | NOT NULL | Report creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**:
- `user_id, created_at` (composite, descending on created_at)
- `input_type`

## Authentication and Authorization

### JWT Authentication Flow

1. **Login**: User submits credentials to `/api/users/login/`
2. **Token Generation**: Server validates credentials and returns:
   ```json
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "user": {
       "id": 1,
       "email": "user@example.com",
       "role": "REGULAR",
       "first_name": "John",
       "last_name": "Doe"
     }
   }
   ```
3. **Token Storage**: Frontend stores tokens in localStorage
4. **Authenticated Requests**: Include `Authorization: Bearer <access_token>` header
5. **Token Refresh**: When access token expires, use refresh token at `/api/users/token/refresh/`

### Token Configuration
- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Algorithm**: HS256

### Role-Based Permissions

#### Permission Classes

**IsAuthenticated**: User must be logged in
- Used for: All protected endpoints

**IsRegularUser**: User role must be 'REGULAR'
- Used for: Service requests, problem reporting

**IsServiceProvider**: User role must be 'PROVIDER' and approved
- Used for: Service management, request responses

**IsAdmin**: User role must be 'ADMIN'
- Used for: Provider approvals, analytics, exports

**IsOwner**: User must own the resource
- Used for: Updating/deleting own services, viewing own requests

### Authorization Matrix

| Endpoint | Guest | Regular User | Provider | Admin |
|----------|-------|--------------|----------|-------|
| View services | ✓ | ✓ | ✓ | ✓ |
| Create service request | ✗ | ✓ | ✗ | ✗ |
| Create service | ✗ | ✗ | ✓ | ✗ |
| Manage own services | ✗ | ✗ | ✓ | ✗ |
| Accept/reject requests | ✗ | ✗ | ✓ | ✗ |
| Submit problem report | ✗ | ✓ | ✗ | ✗ |
| Approve providers | ✗ | ✗ | ✗ | ✓ |
| View analytics | ✗ | ✗ | ✗ | ✓ |
| Export data | ✗ | ✗ | ✗ | ✓ |

## Key Components

### Backend Components

#### 1. Email Notification Service
**Location**: `backend/core/email_service.py`

Handles all email notifications:
- Provider approval/rejection emails
- Service request status change notifications
- Uses Django's email backend with HTML templates

#### 2. AI Recommendation Service
**Location**: `backend/apps/problems/ai_service.py`

Generates problem recommendations:
- Integrates with OpenAI API
- Processes text and transcribed voice input
- Returns structured recommendations within 5 seconds
- Implements retry logic and error handling

#### 3. Service Repository
**Location**: `backend/apps/services/repositories.py`

Data access layer for services:
- Abstracts database queries
- Implements filtering and search logic
- Optimizes queries with select_related/prefetch_related

#### 4. Analytics Service
**Location**: `backend/apps/analytics/services.py`

Aggregates platform metrics:
- User registration trends
- Service request statistics
- Provider activity metrics
- Generates CSV exports

### Frontend Components

#### 1. Authentication Context
**Location**: `frontend/src/contexts/AuthContext.tsx`

Manages authentication state:
- Stores user data and tokens
- Provides login/logout functions
- Handles token refresh
- Protects routes based on role

#### 2. API Client
**Location**: `frontend/src/lib/api/`

Centralized API communication:
- Axios instance with interceptors
- Automatic token injection
- Error handling and retry logic
- Request/response transformation

#### 3. Landing Page Components
**Location**: `frontend/src/components/landing/`

Animated landing page:
- HeroSection with Framer Motion animations
- FeaturesGrid with scroll-triggered animations
- ServicePreview with interactive elements
- Responsive design with TailwindCSS

#### 4. Dashboard Components
**Location**: `frontend/src/components/user/`, `provider/`, `admin/`

Role-specific dashboards:
- **User**: Service search, request tracking, problem reporting
- **Provider**: Request inbox, service management
- **Admin**: Provider approvals, analytics charts, data export

## Performance Optimizations

### Backend Optimizations
1. **Database Indexing**: Strategic indexes on frequently queried fields
2. **Query Optimization**: Use of select_related() and prefetch_related()
3. **Pagination**: All list endpoints return paginated results
4. **Caching**: Future implementation with Redis for frequently accessed data

### Frontend Optimizations
1. **Code Splitting**: Route-based code splitting with React.lazy()
2. **React Query**: Server state caching and automatic refetching
3. **Debouncing**: Search inputs debounced to reduce API calls
4. **Image Optimization**: Lazy loading and optimized image formats
5. **Animation Performance**: Reduced motion support for accessibility

## Security Measures

### Backend Security
1. **Password Hashing**: PBKDF2 with SHA256 (Django default)
2. **JWT Security**: Short-lived access tokens, HTTP-only refresh tokens
3. **CORS Configuration**: Restricted to frontend domain
4. **Input Validation**: Django serializers validate all input
5. **SQL Injection Prevention**: Django ORM parameterized queries
6. **File Upload Validation**: Audio file type and size validation

### Frontend Security
1. **XSS Prevention**: React automatic escaping
2. **CSRF Protection**: Django CSRF tokens for state-changing operations
3. **Secure Storage**: Tokens stored in localStorage (consider httpOnly cookies for production)
4. **HTTPS Only**: All API communication over HTTPS in production

## Testing Strategy

### Backend Tests
**Location**: `backend/tests/`

- **Integration Tests**: Test complete workflows (auth, service requests, etc.)
- **Coverage**: Core business logic and API endpoints
- **Tools**: pytest, pytest-django, factory_boy

### Frontend Tests
**Location**: `frontend/src/**/*.test.tsx`

- **Component Tests**: Test UI components in isolation
- **Integration Tests**: Test user flows
- **Tools**: Vitest, React Testing Library

## Deployment Architecture

### Production Setup
```
┌─────────────┐
│   Nginx     │ (Reverse Proxy, Static Files)
└──────┬──────┘
       │
       ├──────▶ Frontend (Static Build)
       │
       └──────▶ Backend (Gunicorn + Django)
                    │
                    └──────▶ PostgreSQL Database
```

### Environment Variables
- Backend: Database credentials, JWT secret, OpenAI API key, email settings
- Frontend: API base URL, environment mode

---

**Last Updated**: November 2024
**Version**: 1.0.0
