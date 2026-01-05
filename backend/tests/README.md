# Integration Tests for Service Marketplace Platform

This directory contains comprehensive integration tests for all major workflows in the Service Marketplace Platform.

## Test Structure

The tests are organized by feature area:

- `test_integration_auth_flow.py` - User registration, login, and admin approval workflows
- `test_integration_service_workflow.py` - Service discovery, search, and request workflows
- `test_integration_provider_workflow.py` - Service provider CRUD operations
- `test_integration_problem_reporting.py` - Problem reporting with AI recommendations
- `test_integration_admin_analytics.py` - Admin analytics dashboard and reporting
- `test_integration_password_change.py` - Password change functionality for all roles

## Requirements Coverage

Each test file maps to specific requirements from the requirements document:

### Authentication & User Management (Requirements 2.x, 9.x)
- Regular user registration with immediate access
- Service provider registration with pending approval
- Admin approval/rejection workflow with email notifications
- Role-based dashboard redirects
- Password validation and email format validation

### Service Discovery & Requests (Requirements 3.x, 4.x, 7.x)
- Service search with location and cost filters
- Service request submission and tracking
- Provider request inbox and response actions
- Email notifications for status changes
- Role-based request filtering

### Service Provider Operations (Requirements 8.x)
- Service creation, editing, and deletion
- Deletion prevention with pending requests
- Service visibility in user search
- Provider-only access controls

### Problem Reporting (Requirements 5.x)
- Text-based problem submission
- Voice-based problem submission with transcription
- AI recommendations within 5 seconds
- Problem history display
- Error handling for AI and transcription services

### Admin Analytics (Requirements 10.x)
- Dashboard metrics with real data
- Chart accuracy and filtering
- Date range, role, and activity type filters
- Search functionality for users, providers, and requests
- CSV export with filtered data

### Password Management (Requirements 6.x)
- Password change for all user roles
- Current password verification
- Password strength validation
- Session invalidation after change

## Running the Tests

### Install Dependencies

```bash
pip install pytest pytest-django factory-boy faker
```

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_integration_auth_flow.py
```

### Run Specific Test Class

```bash
pytest tests/test_integration_auth_flow.py::TestUserRegistrationAndLoginFlow
```

### Run Specific Test Method

```bash
pytest tests/test_integration_auth_flow.py::TestUserRegistrationAndLoginFlow::test_regular_user_registration_and_immediate_access
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ --cov=apps --cov-report=html
```

### Run Only Integration Tests

```bash
pytest tests/ -m integration
```

## Test Configuration

The tests use the following configuration (defined in `pytest.ini`):

- Django settings: `config.settings.development`
- Database: Test database (automatically created and destroyed)
- Markers: `integration` for integration tests, `e2e` for end-to-end tests

## Fixtures

Common fixtures are defined in `conftest.py`:

- `api_client` - Unauthenticated API client
- `regular_user` - Regular user account
- `provider_user` - Approved service provider account
- `pending_provider_user` - Pending service provider account
- `admin_user` - Admin user account
- `service` - Sample service
- `service_request` - Sample service request
- `authenticated_client` - Authenticated client for regular user
- `provider_client` - Authenticated client for provider
- `admin_client` - Authenticated client for admin

## Mocking

Tests that interact with external services (AI recommendations, voice transcription) use mocking to:

- Avoid external API calls during testing
- Ensure consistent test results
- Test error handling scenarios
- Verify performance requirements

## Notes

- Tests use the `--reuse-db` flag to speed up test execution
- The test database is automatically created on first run
- Email notifications are not actually sent during tests (mocked)
- AI and transcription services are mocked to avoid external dependencies

## Troubleshooting

### Database Connection Errors

Ensure PostgreSQL is running and the test database can be created:

```bash
createdb test_service_marketplace
```

### Import Errors

Make sure you're in the backend directory and have installed all dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Test Failures

Run tests with verbose output and full traceback:

```bash
pytest tests/ -vv --tb=long
```
