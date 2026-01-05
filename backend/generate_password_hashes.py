#!/usr/bin/env python
"""
Generate Django password hashes for sample data
Run this script to get properly hashed passwords for the sample_data.sql file
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth.hashers import make_password

# Generate hashes for sample passwords
passwords = {
    'admin123': make_password('admin123'),
    'user123': make_password('user123'),
    'provider123': make_password('provider123'),
}

print("Generated Password Hashes:")
print("=" * 80)
for password, hash_value in passwords.items():
    print(f"\nPassword: {password}")
    print(f"Hash: {hash_value}")
    print("-" * 80)

print("\n\nUpdate your sample_data.sql file with these hashes.")
