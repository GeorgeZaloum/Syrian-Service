-- Service Marketplace Platform - Complete Database Schema
-- PostgreSQL Database Setup Script
-- Generated: 2025-12-01

-- Drop existing tables if they exist (in correct order to handle foreign keys)
DROP TABLE IF EXISTS problem_reports CASCADE;
DROP TABLE IF EXISTS service_requests CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS provider_profiles CASCADE;
DROP TABLE IF EXISTS users_groups CASCADE;
DROP TABLE IF EXISTS users_user_permissions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'REGULAR' CHECK (role IN ('REGULAR', 'PROVIDER', 'ADMIN')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- ============================================
-- USERS GROUPS (Many-to-Many)
-- ============================================
CREATE TABLE users_groups (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL,
    UNIQUE(user_id, group_id)
);

-- ============================================
-- USERS PERMISSIONS (Many-to-Many)
-- ============================================
CREATE TABLE users_user_permissions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL,
    UNIQUE(user_id, permission_id)
);

-- ============================================
-- PROVIDER PROFILES TABLE
-- ============================================
CREATE TABLE provider_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    service_description TEXT NOT NULL,
    approval_status VARCHAR(10) NOT NULL DEFAULT 'PENDING' CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED')),
    approved_by_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for provider_profiles table
CREATE INDEX idx_provider_profiles_user ON provider_profiles(user_id);
CREATE INDEX idx_provider_profiles_status ON provider_profiles(approval_status);
CREATE INDEX idx_provider_profiles_created_at ON provider_profiles(created_at DESC);

-- ============================================
-- SERVICES TABLE
-- ============================================
CREATE TABLE services (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(200) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL CHECK (cost >= 0.01),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for services table
CREATE INDEX idx_services_provider ON services(provider_id);
CREATE INDEX idx_services_location ON services(location);
CREATE INDEX idx_services_cost ON services(cost);
CREATE INDEX idx_services_is_active ON services(is_active);
CREATE INDEX idx_services_provider_active ON services(provider_id, is_active);
CREATE INDEX idx_services_location_cost ON services(location, cost);
CREATE INDEX idx_services_created_at ON services(created_at DESC);

-- ============================================
-- SERVICE REQUESTS TABLE
-- ============================================
CREATE TABLE service_requests (
    id BIGSERIAL PRIMARY KEY,
    service_id BIGINT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    requester_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED')),
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for service_requests table
CREATE INDEX idx_service_requests_service ON service_requests(service_id);
CREATE INDEX idx_service_requests_requester ON service_requests(requester_id);
CREATE INDEX idx_service_requests_provider ON service_requests(provider_id);
CREATE INDEX idx_service_requests_status ON service_requests(status);
CREATE INDEX idx_service_requests_requester_status ON service_requests(requester_id, status);
CREATE INDEX idx_service_requests_provider_status ON service_requests(provider_id, status);
CREATE INDEX idx_service_requests_service_status ON service_requests(service_id, status);
CREATE INDEX idx_service_requests_created_at ON service_requests(created_at DESC);

-- ============================================
-- PROBLEM REPORTS TABLE
-- ============================================
CREATE TABLE problem_reports (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    input_type VARCHAR(10) NOT NULL DEFAULT 'TEXT' CHECK (input_type IN ('TEXT', 'VOICE')),
    problem_text TEXT NOT NULL,
    audio_file VARCHAR(100),
    recommendations JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for problem_reports table
CREATE INDEX idx_problem_reports_user ON problem_reports(user_id);
CREATE INDEX idx_problem_reports_input_type ON problem_reports(input_type);
CREATE INDEX idx_problem_reports_user_created ON problem_reports(user_id, created_at DESC);
CREATE INDEX idx_problem_reports_created_at ON problem_reports(created_at DESC);

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_provider_profiles_updated_at BEFORE UPDATE ON provider_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_requests_updated_at BEFORE UPDATE ON service_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_problem_reports_updated_at BEFORE UPDATE ON problem_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE users IS 'Main users table with authentication and role information';
COMMENT ON TABLE provider_profiles IS 'Extended profile information for service providers';
COMMENT ON TABLE services IS 'Services offered by providers';
COMMENT ON TABLE service_requests IS 'Requests made by users for services';
COMMENT ON TABLE problem_reports IS 'User-submitted problems with AI recommendations';

-- ============================================
-- GRANT PERMISSIONS (adjust as needed)
-- ============================================

-- Grant all privileges to the database user
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- ============================================
-- COMPLETION MESSAGE
-- ============================================

SELECT 'Database schema created successfully!' AS status;
