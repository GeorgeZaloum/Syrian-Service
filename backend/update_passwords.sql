-- Update passwords for existing users with proper Django hashes

-- Update Admin User (password: admin123)
UPDATE users 
SET password = 'pbkdf2_sha256$600000$GfwZnx3PPE9sB3zpfh4XlU$K+rADA5l3YdbZUtwxUqEmN787D9wa2ZapVX9JtATDxA='
WHERE email = 'admin@marketplace.com';

-- Update Regular Users (password: user123)
UPDATE users 
SET password = 'pbkdf2_sha256$600000$5YLqyvGAxQWbp3r1dhEpBJ$beotf2b8u3LMcVQJyGCk3MsrDLgWK8W2kmeu4ttVTqc='
WHERE email IN ('john.doe@example.com', 'jane.smith@example.com', 'mike.wilson@example.com');

-- Update Service Providers (password: provider123)
UPDATE users 
SET password = 'pbkdf2_sha256$600000$vLvDAPIjvSOQ8x503ZNgs5$a6eujYyjxghtqQ4BlkERVyGkAcdEnTIpJrcg8jSaCKQ='
WHERE email IN ('plumber.pro@example.com', 'electrician.expert@example.com', 'cleaner.best@example.com', 'carpenter.master@example.com');

-- Verify updates
SELECT email, role, 
       CASE 
         WHEN password LIKE 'pbkdf2_sha256$600000$GfwZnx3PPE9sB3zpfh4XlU%' THEN 'admin123'
         WHEN password LIKE 'pbkdf2_sha256$600000$5YLqyvGAxQWbp3r1dhEpBJ%' THEN 'user123'
         WHEN password LIKE 'pbkdf2_sha256$600000$vLvDAPIjvSOQ8x503ZNgs5%' THEN 'provider123'
         ELSE 'unknown'
       END as password_set
FROM users
ORDER BY role, email;
