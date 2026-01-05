"""
Script to load sample data into the database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection

def load_sample_data(clear_existing=False):
    """Load sample data from SQL file"""
    
    if clear_existing:
        print("Clearing existing data...")
        with connection.cursor() as cursor:
            # Delete in reverse order of dependencies
            cursor.execute("DELETE FROM problem_reports;")
            cursor.execute("DELETE FROM service_requests;")
            cursor.execute("DELETE FROM services;")
            cursor.execute("DELETE FROM provider_profiles;")
            cursor.execute("DELETE FROM users;")
        print("✓ Existing data cleared")
    
    sql_file_path = os.path.join(os.path.dirname(__file__), 'sample_data.sql')
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    with connection.cursor() as cursor:
        cursor.execute(sql_content)
    
    print("✓ Sample data loaded successfully!")

if __name__ == '__main__':
    import sys
    clear = '--clear' in sys.argv
    load_sample_data(clear_existing=clear)
