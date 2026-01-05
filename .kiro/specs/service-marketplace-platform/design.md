# Design Document

## Overview

The Service Marketplace Platform is a full-stack web application built with Django REST Framework (backend), React with TypeScript (frontend), PostgreSQL (database), and modern UI libraries (Radix UI, shadcn/ui). The architecture follows a clean separation of concerns with a RESTful API layer, service-oriented backend, and component-based frontend. The system implements SOLID principles, repository pattern for data access, and JWT-based authentication.

## Architecture

### High-Level Architecture
 
```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  ┌────────────┐  ┌──────────┐  ┌─────────────────────────┐ │
│  │   Pages    │  │Components│  │  State Management       │ │
│  │            │  │          │  │  (Context API/Zustand)  │ │
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
│  │              API Layer (ViewSets/Views)                 ││
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

### Technology Stack

**Backend:**
- Django 5.0+ with Django REST Framework
- PostgreSQL 15+ for database
- JWT authentication (djangorestframework-simplejwt)
- Celery for async tasks (email notifications, AI processing)
- Redis for caching and Celery broker

**Frontend:**
- React 18+ with TypeScript
- Vite for build tooling
- Radix UI primitives for accessible components
- shadcn/ui for pre-built components
- TailwindCSS for styling
- Framer Motion for animations
- React Query for server state management
- Zustand for client state management
- Axios for HTTP requests

**AI/ML:**
- OpenAI API or local LLM for problem recommendation system
- Whisper API for voice transcription

### Directory Structure

```
service-marketplace-platform/
├── backend/
│   ├── config/                    # Django settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/                 # User management app
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   └── urls.py
│   │   ├── services/              # Service management app
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   └── urls.py
│   │   ├── requests/              # Service request app
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   └── urls.py
│   │   ├── problems/              # Problem reporting app
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   ├── ai_service.py
│   │   │   └── urls.py
│   │   └── analytics/             # Admin analytics app
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── services.py
│   │       └── urls.py
│   ├── core/                      # Shared utilities
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── exceptions.py
│   │   └── email_service.py
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ui/                # shadcn/ui components
    │   │   ├── layout/            # Layout components
    │   │   ├── auth/              # Auth-related components
    │   │   ├── services/          # Service components
    │   │   ├── dashboard/         # Dashboard components
    │   │   └── landing/           # Landing page components
    │   ├── pages/
    │   │   ├── LandingPage.tsx
    │   │   ├── LoginPage.tsx
    │   │   ├── RegisterPage.tsx
    │   │   ├── user/
    │   │   ├── provider/
    │   │   └── admin/
    │   ├── lib/
    │   │   ├── api/               # API client
    │   │   ├── hooks/             # Custom hooks
    │   │   ├── store/             # State management
    │   │   └── utils/             # Utilities
    │   ├── types/                 # TypeScript types
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

## Components and Interfaces

### Backend Components

#### 1. User Management (apps/users)

**Models:**
```python
class User(AbstractBaseUser, PermissionsMixin):
    """Base user model with role-based access"""
    ROLE_CHOICES = [
        ('REGULAR', 'Regular User'),
        ('PROVIDER', 'Service Provider'),
        ('ADMIN', 'Admin'),
    ]
    email = EmailField(unique=True)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    role = CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)

class ProviderProfile(Model):
    """Extended profile for service providers"""
    user = OneToOneField(User, on_delete=CASCADE)
    service_description = TextField()
    approval_status = CharField(choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ])
    approved_by = ForeignKey(User, null=True, on_delete=SET_NULL)
    approved_at = DateTimeField(null=True)
```

**Services:**
- `UserRegistrationService`: Handles user registration logic
- `ProviderApprovalService`: Manages provider approval workflow
- `PasswordChangeService`: Handles password updates
- `EmailNotificationService`: Sends approval/rejection emails

**API Endpoints:**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT)
- `POST /api/auth/refresh/` - Token refresh
- `POST /api/auth/password/change/` - Password change
- `GET /api/users/me/` - Current user profile
- `GET /api/providers/applications/` - List provider applications (Admin)
- `POST /api/providers/applications/{id}/approve/` - Approve provider
- `POST /api/providers/applications/{id}/reject/` - Reject provider

#### 2. Service Management (apps/services)

**Models:**
```python
class Service(Model):
    """Service offered by providers"""
    provider = ForeignKey(User, on_delete=CASCADE)
    name = CharField(max_length=200)
    description = TextField()
    location = CharField(max_length=200)
    cost = DecimalField(max_digits=10, decimal_places=2)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Services:**
- `ServiceManagementService`: CRUD operations for services
- `ServiceSearchService`: Search and filtering logic

**API Endpoints:**
- `GET /api/services/` - List/search services (with filters)
- `POST /api/services/` - Create service (Provider)
- `GET /api/services/{id}/` - Service detail
- `PUT /api/services/{id}/` - Update service (Provider)
- `DELETE /api/services/{id}/` - Delete service (Provider)

#### 3. Service Requests (apps/requests)

**Models:**
```python
class ServiceRequest(Model):
    """Request from user to provider"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]
    service = ForeignKey(Service, on_delete=CASCADE)
    requester = ForeignKey(User, on_delete=CASCADE, related_name='sent_requests')
    provider = ForeignKey(User, on_delete=CASCADE, related_name='received_requests')
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    message = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Services:**
- `ServiceRequestService`: Manages request lifecycle
- `RequestNotificationService`: Sends notifications on status changes

**API Endpoints:**
- `POST /api/requests/` - Create service request (User)
- `GET /api/requests/` - List requests (filtered by role)
- `GET /api/requests/{id}/` - Request detail
- `POST /api/requests/{id}/accept/` - Accept request (Provider)
- `POST /api/requests/{id}/reject/` - Reject request (Provider)

#### 4. Problem Reporting (apps/problems)

**Models:**
```python
class ProblemReport(Model):
    """User-submitted problem with AI recommendations"""
    INPUT_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('VOICE', 'Voice'),
    ]
    user = ForeignKey(User, on_delete=CASCADE)
    input_type = CharField(max_length=10, choices=INPUT_TYPE_CHOICES)
    problem_text = TextField()
    audio_file = FileField(upload_to='problem_audio/', null=True)
    recommendations = JSONField()
    created_at = DateTimeField(auto_now_add=True)
```

**Services:**
- `ProblemReportService`: Handles problem submission
- `AIRecommendationService`: Generates recommendations using AI
- `VoiceTranscriptionService`: Transcribes voice input

**API Endpoints:**
- `POST /api/problems/` - Submit problem report
- `GET /api/problems/` - List user's problem reports
- `GET /api/problems/{id}/` - Problem detail with recommendations

#### 5. Analytics (apps/analytics)

**Services:**
- `AnalyticsService`: Aggregates platform metrics
- `ReportGenerationService`: Generates CSV exports

**API Endpoints:**
- `GET /api/analytics/dashboard/` - Dashboard metrics (Admin)
- `GET /api/analytics/users/` - User statistics
- `GET /api/analytics/requests/` - Request statistics
- `GET /api/analytics/providers/` - Provider statistics
- `GET /api/analytics/export/` - Export data as CSV

### Frontend Components

#### 1. Landing Page Components

**Components:**
- `HeroSection`: Animated hero with service showcase
- `FeaturesGrid`: Animated feature cards
- `ServicePreview`: Interactive service browser
- `CTASection`: Call-to-action with registration prompts
- `AnimatedBackground`: Particle effects or gradient animations

**Animations:**
- Fade-in on scroll (Framer Motion)
- Parallax effects
- Hover interactions
- Smooth transitions between sections

#### 2. Authentication Components

**Components:**
- `LoginForm`: Email/password login with validation
- `RegisterForm`: Role-based registration with conditional fields
- `RoleSelector`: Toggle between Regular User and Service Provider
- `PasswordStrengthIndicator`: Visual password validation

#### 3. Dashboard Components

**User Dashboard:**
- `ServiceSearchPanel`: Search with location/cost filters
- `ServiceCard`: Service display with request button
- `RequestList`: User's service requests with status
- `ProblemReportForm`: Text/voice input for problems
- `RecommendationDisplay`: AI-generated solutions

**Provider Dashboard:**
- `RequestInbox`: Pending requests with accept/reject actions
- `ServiceManager`: CRUD interface for services
- `ServiceForm`: Add/edit service form
- `ServiceList`: Provider's services with edit/delete actions

**Admin Dashboard:**
- `ProviderApplicationList`: Pending applications with approve/reject
- `AnalyticsCharts`: Charts using Recharts or Chart.js
- `FilterPanel`: Date range, role, activity filters
- `MetricsCards`: Real-time platform metrics
- `ExportButton`: CSV export functionality

#### 4. Shared UI Components (shadcn/ui)

- `Button`, `Input`, `Select`, `Textarea`
- `Card`, `Dialog`, `DropdownMenu`
- `Table`, `Tabs`, `Toast`
- `Form` components with validation

## Data Models

### Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────────┐
│    User     │────────▶│ ProviderProfile  │
│             │ 1     1 │                  │
│ - id        │         │ - service_desc   │
│ - email     │         │ - approval_status│
│ - role      │         └──────────────────┘
│ - name      │
└─────────────┘
      │ 1
      │
      │ *
┌─────────────┐
│   Service   │
│             │
│ - id        │
│ - provider  │────┐
│ - name      │    │
│ - location  │    │
│ - cost      │    │
└─────────────┘    │
      │ 1          │
      │            │
      │ *          │
┌──────────────────┐
│ ServiceRequest   │
│                  │
│ - id             │
│ - service        │
│ - requester      │◀───┐
│ - provider       │────┘
│ - status         │
└──────────────────┘

┌──────────────────┐
│  ProblemReport   │
│                  │
│ - id             │
│ - user           │────▶ User
│ - problem_text   │
│ - recommendations│
└──────────────────┘
```

### Database Indexes

- `User.email` (unique)
- `Service.provider`, `Service.location`, `Service.cost`
- `ServiceRequest.requester`, `ServiceRequest.provider`, `ServiceRequest.status`
- `ProblemReport.user`, `ProblemReport.created_at`

## Error Handling

### Backend Error Handling

**Custom Exception Classes:**
```python
class ServiceMarketplaceException(Exception):
    """Base exception"""
    pass

class UnauthorizedException(ServiceMarketplaceException):
    """User not authorized"""
    pass

class ValidationException(ServiceMarketplaceException):
    """Data validation failed"""
    pass

class NotFoundException(ServiceMarketplaceException):
    """Resource not found"""
    pass
```

**Error Response Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["This field is required"]
    }
  }
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

### Frontend Error Handling

**Error Boundary:**
- Catch React component errors
- Display fallback UI
- Log errors for debugging

**API Error Handling:**
- Intercept Axios errors
- Display toast notifications
- Retry logic for network failures
- Redirect to login on 401

**Form Validation:**
- Client-side validation with Zod
- Real-time field validation
- Display inline error messages

## Testing Strategy

### Backend Testing

**Unit Tests:**
- Test services in isolation with mocked repositories
- Test model methods and properties
- Test serializer validation logic
- Coverage target: 80%+

**Integration Tests:**
- Test API endpoints with test database
- Test authentication flows
- Test permission checks
- Test email sending (mocked)

**Test Tools:**
- pytest with pytest-django
- factory_boy for test data
- faker for realistic data generation

### Frontend Testing

**Unit Tests:**
- Test utility functions
- Test custom hooks
- Test state management logic
- Coverage target: 70%+

**Component Tests:**
- Test component rendering
- Test user interactions
- Test form validation
- Mock API calls

**E2E Tests:**
- Test critical user flows (registration, login, service request)
- Test across different roles
- Test responsive design

**Test Tools:**
- Vitest for unit tests
- React Testing Library for component tests
- Playwright for E2E tests

## Security Considerations

1. **Authentication:**
   - JWT tokens with short expiration (15 min access, 7 day refresh)
   - Secure password hashing (Django's PBKDF2)
   - HTTPS only in production

2. **Authorization:**
   - Role-based permissions on all endpoints
   - Object-level permissions (users can only modify their own data)
   - Admin-only endpoints protected

3. **Input Validation:**
   - Django serializer validation
   - SQL injection prevention (Django ORM)
   - XSS prevention (React escaping)
   - CSRF protection

4. **Data Protection:**
   - Sensitive data encrypted at rest
   - PII handling compliance
   - Secure file upload validation

5. **Rate Limiting:**
   - API rate limiting per user
   - Brute force protection on login

## Performance Optimization

1. **Backend:**
   - Database query optimization (select_related, prefetch_related)
   - Redis caching for frequently accessed data
   - Pagination for list endpoints
   - Async tasks for email and AI processing

2. **Frontend:**
   - Code splitting by route
   - Lazy loading for heavy components
   - Image optimization
   - React Query caching
   - Debounced search inputs

3. **Database:**
   - Proper indexing
   - Connection pooling
   - Query optimization

## Deployment Considerations

**Backend:**
- Gunicorn as WSGI server
- Nginx as reverse proxy
- PostgreSQL with connection pooling
- Redis for caching and Celery
- Celery workers for async tasks
- Environment-based configuration

**Frontend:**
- Vite production build
- Static file serving via Nginx
- Environment variables for API URLs

**Infrastructure:**
- Separate backend and frontend servers
- Database server with backups
- Redis server
- SSL certificates

