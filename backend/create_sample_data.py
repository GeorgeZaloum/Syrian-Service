"""
Django-based script to create sample data
"""
import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.hashers import make_password
from apps.users.models import User, ProviderProfile
from apps.services.models import Service
from apps.requests.models import ServiceRequest
from apps.problems.models import ProblemReport

def create_sample_data():
    """Create sample data using Django ORM"""
    
    print("Creating sample users...")
    
    # Create Admin User
    admin_user, created = User.objects.get_or_create(
        email='admin@marketplace.com',
        defaults={
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('admin123')
        }
    )
    if created:
        print("✓ Admin user created")
    
    # Create Regular Users
    regular_users = [
        {'email': 'john.doe@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'email': 'jane.smith@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'email': 'mike.wilson@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    ]
    
    for user_data in regular_users:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'role': 'REGULAR',
                'password': make_password('user123')
            }
        )
        if created:
            print(f"✓ Regular user {user_data['email']} created")
    
    # Create Provider Users
    provider_users = [
        {'email': 'plumber.pro@example.com', 'first_name': 'Bob', 'last_name': 'Plumber', 'service': 'Professional plumbing services'},
        {'email': 'electrician.expert@example.com', 'first_name': 'Alice', 'last_name': 'Electrician', 'service': 'Expert electrical services'},
        {'email': 'cleaner.best@example.com', 'first_name': 'Carol', 'last_name': 'Cleaner', 'service': 'Best cleaning services'},
        {'email': 'carpenter.master@example.com', 'first_name': 'Dave', 'last_name': 'Carpenter', 'service': 'Master carpentry services'},
    ]
    
    for provider_data in provider_users:
        user, created = User.objects.get_or_create(
            email=provider_data['email'],
            defaults={
                'first_name': provider_data['first_name'],
                'last_name': provider_data['last_name'],
                'role': 'PROVIDER',
                'password': make_password('provider123')
            }
        )
        if created:
            print(f"✓ Provider user {provider_data['email']} created")
            
            # Create provider profile
            profile, profile_created = ProviderProfile.objects.get_or_create(
                user=user,
                defaults={
                    'service_description': provider_data['service'],
                    'approval_status': 'APPROVED',
                    'approved_by': admin_user
                }
            )
            if profile_created:
                print(f"✓ Provider profile for {provider_data['email']} created")
    
    print("\nCreating sample services...")
    
    # Create Services
    services_data = [
        {'provider_email': 'plumber.pro@example.com', 'name': 'Emergency Plumbing', 'description': 'Quick plumbing repairs', 'location': 'Damascus', 'cost': '50.00'},
        {'provider_email': 'plumber.pro@example.com', 'name': 'Bathroom Installation', 'description': 'Complete bathroom setup', 'location': 'Damascus', 'cost': '200.00'},
        {'provider_email': 'electrician.expert@example.com', 'name': 'Electrical Wiring', 'description': 'House wiring services', 'location': 'Aleppo', 'cost': '75.00'},
        {'provider_email': 'electrician.expert@example.com', 'name': 'Light Installation', 'description': 'Install lights and fixtures', 'location': 'Aleppo', 'cost': '30.00'},
        {'provider_email': 'cleaner.best@example.com', 'name': 'House Cleaning', 'description': 'Complete house cleaning', 'location': 'Homs', 'cost': '25.00'},
        {'provider_email': 'cleaner.best@example.com', 'name': 'Office Cleaning', 'description': 'Professional office cleaning', 'location': 'Homs', 'cost': '40.00'},
        {'provider_email': 'carpenter.master@example.com', 'name': 'Furniture Repair', 'description': 'Fix and restore furniture', 'location': 'Latakia', 'cost': '35.00'},
        {'provider_email': 'carpenter.master@example.com', 'name': 'Custom Cabinets', 'description': 'Build custom kitchen cabinets', 'location': 'Latakia', 'cost': '150.00'},
    ]
    
    for service_data in services_data:
        provider = User.objects.get(email=service_data['provider_email'])
        service, created = Service.objects.get_or_create(
            provider=provider,
            name=service_data['name'],
            defaults={
                'description': service_data['description'],
                'location': service_data['location'],
                'cost': Decimal(service_data['cost'])
            }
        )
        if created:
            print(f"✓ Service '{service_data['name']}' created")
    
    print("\nCreating sample service requests...")
    
    # Create Service Requests
    john = User.objects.get(email='john.doe@example.com')
    jane = User.objects.get(email='jane.smith@example.com')
    
    emergency_plumbing = Service.objects.get(name='Emergency Plumbing')
    house_cleaning = Service.objects.get(name='House Cleaning')
    
    requests_data = [
        {'service': emergency_plumbing, 'requester': john, 'status': 'PENDING', 'message': 'Need urgent plumbing help'},
        {'service': house_cleaning, 'requester': jane, 'status': 'ACCEPTED', 'message': 'Weekly cleaning service needed'},
    ]
    
    for request_data in requests_data:
        service_request, created = ServiceRequest.objects.get_or_create(
            service=request_data['service'],
            requester=request_data['requester'],
            defaults={
                'provider': request_data['service'].provider,
                'status': request_data['status'],
                'message': request_data['message']
            }
        )
        if created:
            print(f"✓ Service request for '{request_data['service'].name}' created")
    
    print("\nCreating sample problem reports...")
    
    # Create Problem Reports
    problems_data = [
        {
            'user': john,
            'problem_text': 'My kitchen sink is leaking and water is everywhere',
            'recommendations': [
                {'service': 'Emergency Plumbing', 'provider': 'Bob Plumber', 'reason': 'Specializes in urgent plumbing repairs'},
                {'service': 'Bathroom Installation', 'provider': 'Bob Plumber', 'reason': 'Has experience with water system repairs'}
            ]
        },
        {
            'user': jane,
            'problem_text': 'The lights in my living room stopped working',
            'recommendations': [
                {'service': 'Electrical Wiring', 'provider': 'Alice Electrician', 'reason': 'Expert in electrical troubleshooting'},
                {'service': 'Light Installation', 'provider': 'Alice Electrician', 'reason': 'Specializes in lighting solutions'}
            ]
        }
    ]
    
    for problem_data in problems_data:
        problem, created = ProblemReport.objects.get_or_create(
            user=problem_data['user'],
            problem_text=problem_data['problem_text'],
            defaults={
                'input_type': 'TEXT',
                'recommendations': problem_data['recommendations']
            }
        )
        if created:
            print(f"✓ Problem report created for {problem_data['user'].email}")
    
    print("\n✅ Sample data creation completed!")
    print("\n📊 Summary:")
    print(f"Users: {User.objects.count()}")
    print(f"Provider Profiles: {ProviderProfile.objects.count()}")
    print(f"Services: {Service.objects.count()}")
    print(f"Service Requests: {ServiceRequest.objects.count()}")
    print(f"Problem Reports: {ProblemReport.objects.count()}")
    
    print("\n🔑 Login Credentials:")
    print("Admin: admin@marketplace.com / admin123")
    print("Users: john.doe@example.com / user123")
    print("       jane.smith@example.com / user123")
    print("       mike.wilson@example.com / user123")
    print("Providers: plumber.pro@example.com / provider123")
    print("           electrician.expert@example.com / provider123")
    print("           cleaner.best@example.com / provider123")
    print("           carpenter.master@example.com / provider123")

if __name__ == '__main__':
    create_sample_data()