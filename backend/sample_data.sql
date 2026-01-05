-- Service Marketplace Platform - Sample Data
-- PostgreSQL Sample Data Script
-- Generated: 2025-12-01

-- ============================================
-- SAMPLE USERS
-- ============================================

-- Insert Admin User (password: admin123)
INSERT INTO users (email, password, first_name, last_name, role, is_active, is_staff, is_superuser, created_at, updated_at)
VALUES 
('admin@marketplace.com', 'pbkdf2_sha256$600000$GfwZnx3PPE9sB3zpfh4XlU$K+rADA5l3YdbZUtwxUqEmN787D9wa2ZapVX9JtATDxA=', 'Admin', 'User', 'ADMIN', TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert Regular Users (password: user123)
INSERT INTO users (email, password, first_name, last_name, role, is_active, is_staff, is_superuser, created_at, updated_at)
VALUES 
('john.doe@example.com', 'pbkdf2_sha256$600000$5YLqyvGAxQWbp3r1dhEpBJ$beotf2b8u3LMcVQJyGCk3MsrDLgWK8W2kmeu4ttVTqc=', 'John', 'Doe', 'REGULAR', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('jane.smith@example.com', 'pbkdf2_sha256$600000$5YLqyvGAxQWbp3r1dhEpBJ$beotf2b8u3LMcVQJyGCk3MsrDLgWK8W2kmeu4ttVTqc=', 'Jane', 'Smith', 'REGULAR', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('mike.wilson@example.com', 'pbkdf2_sha256$600000$5YLqyvGAxQWbp3r1dhEpBJ$beotf2b8u3LMcVQJyGCk3MsrDLgWK8W2kmeu4ttVTqc=', 'Mike', 'Wilson', 'REGULAR', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert Service Providers (password: provider123)
INSERT INTO users (email, password, first_name, last_name, role, is_active, is_staff, is_superuser, created_at, updated_at)
VALUES 
('plumber.pro@example.com', 'pbkdf2_sha256$600000$vLvDAPIjvSOQ8x503ZNgs5$a6eujYyjxghtqQ4BlkERVyGkAcdEnTIpJrcg8jSaCKQ=', 'Bob', 'Builder', 'PROVIDER', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('electrician.expert@example.com', 'pbkdf2_sha256$600000$vLvDAPIjvSOQ8x503ZNgs5$a6eujYyjxghtqQ4BlkERVyGkAcdEnTIpJrcg8jSaCKQ=', 'Sarah', 'Sparks', 'PROVIDER', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('cleaner.best@example.com', 'pbkdf2_sha256$600000$vLvDAPIjvSOQ8x503ZNgs5$a6eujYyjxghtqQ4BlkERVyGkAcdEnTIpJrcg8jSaCKQ=', 'Maria', 'Clean', 'PROVIDER', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('carpenter.master@example.com', 'pbkdf2_sha256$600000$vLvDAPIjvSOQ8x503ZNgs5$a6eujYyjxghtqQ4BlkERVyGkAcdEnTIpJrcg8jSaCKQ=', 'Tom', 'Woods', 'PROVIDER', TRUE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ============================================
-- PROVIDER PROFILES
-- ============================================

INSERT INTO provider_profiles (user_id, service_description, approval_status, approved_by_id, approved_at, created_at, updated_at)
VALUES 
((SELECT id FROM users WHERE email = 'plumber.pro@example.com'), 
 'Professional plumbing services with 10+ years of experience. Specializing in residential and commercial plumbing repairs, installations, and maintenance.',
 'APPROVED', 
 (SELECT id FROM users WHERE email = 'admin@marketplace.com'),
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'electrician.expert@example.com'),
 'Licensed electrician offering electrical installations, repairs, and safety inspections. Available for emergency services 24/7.',
 'APPROVED',
 (SELECT id FROM users WHERE email = 'admin@marketplace.com'),
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'cleaner.best@example.com'),
 'Professional cleaning services for homes and offices. Eco-friendly products, flexible scheduling, and satisfaction guaranteed.',
 'APPROVED',
 (SELECT id FROM users WHERE email = 'admin@marketplace.com'),
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'carpenter.master@example.com'),
 'Expert carpentry services including custom furniture, home renovations, and woodwork repairs. Quality craftsmanship guaranteed.',
 'PENDING',
 NULL,
 NULL,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP);

-- ============================================
-- SERVICES
-- ============================================

INSERT INTO services (provider_id, name, description, location, cost, is_active, created_at, updated_at)
VALUES 
-- Plumber Services
((SELECT id FROM users WHERE email = 'plumber.pro@example.com'),
 'Emergency Plumbing Repair',
 'Fast response for urgent plumbing issues including leaks, burst pipes, and clogged drains. Available 24/7.',
 'Damascus, Syria',
 75.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'plumber.pro@example.com'),
 'Bathroom Installation',
 'Complete bathroom installation including fixtures, piping, and water heater setup.',
 'Damascus, Syria',
 500.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Electrician Services
((SELECT id FROM users WHERE email = 'electrician.expert@example.com'),
 'Electrical Wiring Installation',
 'Professional electrical wiring for new constructions and renovations. Compliant with all safety standards.',
 'Aleppo, Syria',
 300.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'electrician.expert@example.com'),
 'Home Electrical Inspection',
 'Comprehensive electrical safety inspection for homes and businesses.',
 'Aleppo, Syria',
 100.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Cleaning Services
((SELECT id FROM users WHERE email = 'cleaner.best@example.com'),
 'Deep House Cleaning',
 'Thorough cleaning of entire house including all rooms, kitchen, and bathrooms. Eco-friendly products used.',
 'Homs, Syria',
 80.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'cleaner.best@example.com'),
 'Office Cleaning Service',
 'Regular office cleaning service including desks, floors, windows, and common areas.',
 'Homs, Syria',
 120.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Carpenter Services
((SELECT id FROM users WHERE email = 'carpenter.master@example.com'),
 'Custom Furniture Design',
 'Bespoke furniture design and creation tailored to your specific needs and space.',
 'Latakia, Syria',
 400.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

((SELECT id FROM users WHERE email = 'carpenter.master@example.com'),
 'Door and Window Installation',
 'Professional installation of doors and windows with precision fitting and finishing.',
 'Latakia, Syria',
 200.00,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP);

-- ============================================
-- SERVICE REQUESTS
-- ============================================

INSERT INTO service_requests (service_id, requester_id, provider_id, status, message, created_at, updated_at)
VALUES 
-- Pending Request
((SELECT id FROM services WHERE name = 'Emergency Plumbing Repair' LIMIT 1),
 (SELECT id FROM users WHERE email = 'john.doe@example.com'),
 (SELECT id FROM users WHERE email = 'plumber.pro@example.com'),
 'PENDING',
 'I have a leaking pipe in my kitchen. Can you come today?',
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Accepted Request
((SELECT id FROM services WHERE name = 'Deep House Cleaning' LIMIT 1),
 (SELECT id FROM users WHERE email = 'jane.smith@example.com'),
 (SELECT id FROM users WHERE email = 'cleaner.best@example.com'),
 'ACCEPTED',
 'Need cleaning service for this weekend. 3-bedroom apartment.',
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 CURRENT_TIMESTAMP - INTERVAL '1 day'),

-- Completed Request
((SELECT id FROM services WHERE name = 'Home Electrical Inspection' LIMIT 1),
 (SELECT id FROM users WHERE email = 'mike.wilson@example.com'),
 (SELECT id FROM users WHERE email = 'electrician.expert@example.com'),
 'COMPLETED',
 'Please inspect my home electrical system before I move in.',
 CURRENT_TIMESTAMP - INTERVAL '5 days',
 CURRENT_TIMESTAMP - INTERVAL '3 days'),

-- Rejected Request
((SELECT id FROM services WHERE name = 'Custom Furniture Design' LIMIT 1),
 (SELECT id FROM users WHERE email = 'john.doe@example.com'),
 (SELECT id FROM users WHERE email = 'carpenter.master@example.com'),
 'REJECTED',
 'Looking for a custom bookshelf for my office.',
 CURRENT_TIMESTAMP - INTERVAL '7 days',
 CURRENT_TIMESTAMP - INTERVAL '6 days');

-- ============================================
-- PROBLEM REPORTS
-- ============================================

INSERT INTO problem_reports (user_id, input_type, problem_text, audio_file, recommendations, created_at, updated_at)
VALUES 
((SELECT id FROM users WHERE email = 'john.doe@example.com'),
 'TEXT',
 'My kitchen sink is clogged and water is not draining properly.',
 NULL,
 '[{"solution": "Use a plunger to try to clear the blockage", "priority": "high"}, {"solution": "Pour hot water mixed with baking soda and vinegar down the drain", "priority": "medium"}, {"solution": "Contact a professional plumber if the issue persists", "priority": "low"}]'::jsonb,
 CURRENT_TIMESTAMP - INTERVAL '1 day',
 CURRENT_TIMESTAMP - INTERVAL '1 day'),

((SELECT id FROM users WHERE email = 'jane.smith@example.com'),
 'TEXT',
 'The lights in my living room keep flickering.',
 NULL,
 '[{"solution": "Check if the light bulbs are properly screwed in", "priority": "high"}, {"solution": "Replace old or faulty light bulbs", "priority": "medium"}, {"solution": "Have an electrician inspect the wiring if problem continues", "priority": "low"}]'::jsonb,
 CURRENT_TIMESTAMP - INTERVAL '3 days',
 CURRENT_TIMESTAMP - INTERVAL '3 days'),

((SELECT id FROM users WHERE email = 'mike.wilson@example.com'),
 'VOICE',
 'I need help with a broken door handle in my bedroom.',
 'problem_audio/audio_20251201_001.mp3',
 '[{"solution": "Try tightening the screws on the door handle", "priority": "high"}, {"solution": "Replace the door handle if it is damaged", "priority": "medium"}, {"solution": "Contact a carpenter for professional installation", "priority": "low"}]'::jsonb,
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 CURRENT_TIMESTAMP - INTERVAL '2 days');

-- ============================================
-- COMPLETION MESSAGE
-- ============================================

SELECT 'Sample data inserted successfully!' AS status,
       (SELECT COUNT(*) FROM users) AS total_users,
       (SELECT COUNT(*) FROM provider_profiles) AS total_providers,
       (SELECT COUNT(*) FROM services) AS total_services,
       (SELECT COUNT(*) FROM service_requests) AS total_requests,
       (SELECT COUNT(*) FROM problem_reports) AS total_problems;
