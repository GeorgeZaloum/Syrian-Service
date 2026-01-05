# Service Marketplace Platform - Backend

Django REST Framework backend for the Service Marketplace Platform.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 15 or higher
- pip (Python package manager)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

5. Update the `.env` file with your database credentials and other settings.

### Database Setup

1. Create a PostgreSQL database:
```sql
CREATE DATABASE service_marketplace;
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

### Running the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### Project Structure

```
backend/
├── config/                 # Django project configuration
│   ├── settings/          # Settings modules (base, development, production)
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── apps/                  # Django applications
│   ├── users/            # User management
│   ├── services/         # Service management
│   ├── requests/         # Service request management
│   ├── problems/         # Problem reporting
│   └── analytics/        # Admin analytics
├── core/                  # Shared utilities
│   ├── permissions.py    # Custom permission classes
│   ├── pagination.py     # Pagination classes
│   └── exceptions.py     # Custom exception handlers
└── manage.py             # Django management script
```

## API Documentation

API endpoints will be documented as they are implemented in subsequent tasks.

## Testing

Run tests with:
```bash
python manage.py test
```

## Environment Variables

See `.env.example` for all available environment variables.
