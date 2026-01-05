# Requirements Document

## Introduction

This specification addresses a critical bug in the Service Marketplace Platform where provider registration requests are not visible in the admin dashboard. When a service provider signs up, their application should appear in the admin dashboard for approval, but due to a data serialization mismatch between the backend and frontend, the applications are not being displayed correctly.

## Glossary

- **System**: The Service Marketplace Platform web application
- **Provider Application**: A registration request from a prospective Service Provider awaiting Admin approval
- **Admin Dashboard**: The administrative interface where admins review and approve/reject provider applications
- **Backend API**: The Django REST Framework API that serves provider application data
- **Frontend Client**: The React application that displays provider applications to admins
- **Serializer**: A Django REST Framework component that converts model instances to JSON format
- **ProviderProfile**: The database model that stores provider application information

## Requirements

### Requirement 1: Provider Application Data Serialization

**User Story:** As a System, I want to serialize provider application data consistently between backend and frontend, so that admin users can view pending applications.

#### Acceptance Criteria

1. WHEN THE System serializes a ProviderProfile instance, THE System SHALL include the associated user data in the response
2. THE System SHALL use the field name "user_details" for the nested user object in the API response
3. THE System SHALL include all required user fields (id, email, first_name, last_name, role, is_active, created_at) in the user_details object
4. WHEN an Admin requests the list of provider applications, THE System SHALL return all ProviderProfile records with approval_status set to "PENDING"
5. THE System SHALL maintain backward compatibility with existing API consumers

### Requirement 2: Admin Dashboard Display

**User Story:** As an Admin, I want to see all pending provider applications in my dashboard, so that I can review and approve or reject them.

#### Acceptance Criteria

1. WHEN an Admin accesses the provider applications tab, THE System SHALL fetch all pending provider applications from the backend API
2. WHEN the API returns provider applications, THE System SHALL display each application with the provider's name, email, and service description
3. THE System SHALL display approve and reject action buttons for each pending application
4. WHEN no pending applications exist, THE System SHALL display a message indicating "No pending applications"
5. THE System SHALL handle API errors gracefully and display appropriate error messages to the admin

### Requirement 3: Data Consistency Verification

**User Story:** As a Developer, I want to verify that provider registration creates the correct database records, so that the admin approval workflow functions properly.

#### Acceptance Criteria

1. WHEN a Service Provider submits a registration form, THE System SHALL create a User record with role set to "PROVIDER" and is_active set to False
2. WHEN a Service Provider submits a registration form, THE System SHALL create a ProviderProfile record with approval_status set to "PENDING"
3. THE System SHALL link the ProviderProfile record to the User record via a foreign key relationship
4. WHEN the ProviderProfile is created, THE System SHALL store the service_description provided during registration
5. THE System SHALL ensure the ProviderProfile record is queryable by the admin API endpoint
