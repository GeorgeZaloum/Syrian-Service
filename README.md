# Service Marketplace Platform

A full-stack web application connecting users with service providers, featuring AI-powered problem recommendations, real-time service search, and comprehensive admin analytics.

## 🌟 Features

- **Role-Based Access Control**: Three user roles (Regular User, Service Provider, Admin)
- **Service Discovery**: Search and filter services by location and cost
- **Service Request Workflow**: Complete request lifecycle with email notifications
- **AI Problem Recommendations**: Text and voice-based problem reporting with AI solutions
- **Provider Approval System**: Admin workflow for approving service providers
- **Analytics Dashboard**: Comprehensive metrics and CSV export functionality
- **Modern UI**: Animated landing page with Framer Motion and TailwindCSS
- **Responsive Design**: Mobile-first design that works on all devices

## 🏗️ Architecture

- **Backend**: Django 5.0 + Django REST Framework + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite + TailwindCSS
- **Authentication**: JWT-based authentication
- **AI Integration**: OpenAI API for problem recommendations

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## 📋 Prerequisites

### Backend Requirements
- Python 3.10 or higher
- PostgreSQL 15 or higher
- pip (Python package manager)

### Frontend Requirements
- Node.js 18 or higher
- npm or yarn package manager

### External Services
- OpenAI API key (for AI recommendations feature)
- SMTP server credentials (for email notifications)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd service-marketplace-platform
```

### 2. Backend Setup

#### Step 1: Navigate to Backend Directory
```bash
cd backend
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=service_marketplace
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # minutes (7 days)

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Note**: See `.env.example` for a complete template.

#### Step 5: Set Up PostgreSQL Database

**Option A: Using PostgreSQL CLI**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE service_marketplace;

# Create user (optional)
CREATE USER marketplace_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE service_marketplace TO marketplace_user;

# Exit
\q
```

**Option B: Using pgAdmin**
1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Enter database name: `service_marketplace`
4. Click "Save"

#### Step 6: Run Database Migrations
```bash
python manage.py migrate
```

#### Step 7: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Email: admin@example.com
- First name: Admin
- Last name: User
- Password: (enter secure password)

#### Step 8: Start Development Server
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

**Test the API**: Visit `http://localhost:8000/api/users/me/` (should return 401 Unauthorized)

### 3. Frontend Setup

#### Step 1: Navigate to Frontend Directory
```bash
# From project root
cd frontend
```

#### Step 2: Install Dependencies
```bash
npm install
# or
yarn install
```

#### Step 3: Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

**Note**: See `.env.example` for a complete template.

#### Step 4: Start Development Server
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:5173`

#### Step 5: Access the Application

Open your browser and navigate to `http://localhost:5173`

You should see the animated landing page with:
- Hero section with call-to-action buttons
- Features showcase
- Service preview section

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/test_integration_auth_flow.py

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm run test
# or
yarn test

# Run with coverage
npm run test:coverage
```

## 📚 Usage Guide

### Creating User Accounts

#### Regular User Registration
1. Click "Get Started" or "Sign Up" on the landing page
2. Select "Regular User" role
3. Fill in: First Name, Last Name, Email, Password
4. Click "Register"
5. You'll be automatically logged in and redirected to the user dashboard

#### Service Provider Registration
1. Click "Get Started" or "Sign Up" on the landing page
2. Select "Service Provider" role
3. Fill in: First Name, Last Name, Email, Password, Service Description
4. Click "Register"
5. Wait for admin approval (you'll receive an email notification)
6. Once approved, log in to access the provider dashboard

### User Workflows

#### As a Regular User
1. **Search for Services**: Use location and cost filters to find services
2. **Request a Service**: Click on a service card and submit a request
3. **Track Requests**: View request status in "My Requests" tab
4. **Report Problems**: Submit text or voice problems to get AI recommendations
5. **Change Password**: Update your password in settings

#### As a Service Provider
1. **Manage Services**: Create, edit, and delete your services
2. **Handle Requests**: Accept or reject service requests from users
3. **View History**: Track all requests and their statuses
4. **Change Password**: Update your password in settings

#### As an Admin
1. **Approve Providers**: Review and approve/reject provider applications
2. **View Analytics**: Monitor platform metrics and trends
3. **Search Data**: Find specific users, providers, or requests
4. **Export Reports**: Download CSV files of filtered data

## 🔧 Configuration

### Environment Variables Reference

#### Backend (.env)
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| SECRET_KEY | Django secret key | Yes | - |
| DEBUG | Debug mode | No | False |
| ALLOWED_HOSTS | Allowed host names | Yes | - |
| DB_NAME | Database name | Yes | - |
| DB_USER | Database user | Yes | - |
| DB_PASSWORD | Database password | Yes | - |
| DB_HOST | Database host | Yes | localhost |
| DB_PORT | Database port | Yes | 5432 |
| EMAIL_HOST | SMTP server | Yes | - |
| EMAIL_PORT | SMTP port | Yes | 587 |
| EMAIL_HOST_USER | Email username | Yes | - |
| EMAIL_HOST_PASSWORD | Email password | Yes | - |
| OPENAI_API_KEY | OpenAI API key | Yes | - |
| CORS_ALLOWED_ORIGINS | Allowed CORS origins | Yes | - |

#### Frontend (.env)
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| VITE_API_BASE_URL | Backend API URL | Yes | - |

### Email Configuration

#### Using Gmail
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `EMAIL_HOST_PASSWORD`

#### Using Other SMTP Providers
Update the following in your `.env`:
- `EMAIL_HOST`: Your SMTP server (e.g., smtp.sendgrid.net)
- `EMAIL_PORT`: Usually 587 for TLS or 465 for SSL
- `EMAIL_USE_TLS`: True for port 587, False for port 465
- `EMAIL_HOST_USER`: Your SMTP username
- `EMAIL_HOST_PASSWORD`: Your SMTP password

### OpenAI API Configuration

1. Sign up at https://platform.openai.com/
2. Create an API key
3. Add the key to `OPENAI_API_KEY` in your `.env` file
4. Ensure you have credits in your OpenAI account

**Note**: The AI recommendation feature requires a valid OpenAI API key. Without it, problem reporting will fail.

## 🚢 Deployment

### Production Deployment Checklist

#### Backend Deployment

1. **Update Django Settings**
   ```python
   # config/settings/production.py
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **Set Environment Variables**
   - Set all production environment variables on your hosting platform
   - Use strong `SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - Configure production database credentials

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Configure Web Server**
   
   **Using Gunicorn + Nginx**:
   
   Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
   
   Run Gunicorn:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```
   
   Nginx configuration example:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static/ {
           alias /path/to/backend/staticfiles/;
       }
       
       location /media/ {
           alias /path/to/backend/media/;
       }
   }
   ```

#### Frontend Deployment

1. **Update Environment Variables**
   ```env
   VITE_API_BASE_URL=https://yourdomain.com/api
   ```

2. **Build for Production**
   ```bash
   npm run build
   # or
   yarn build
   ```
   
   This creates an optimized build in the `dist/` directory.

3. **Deploy Static Files**
   
   **Option A: Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       root /path/to/frontend/dist;
       index index.html;
       
       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```
   
   **Option B: Vercel**
   ```bash
   npm install -g vercel
   vercel --prod
   ```
   
   **Option C: Netlify**
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod --dir=dist
   ```

### Hosting Recommendations

- **Backend**: Heroku, DigitalOcean, AWS EC2, Railway
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: AWS RDS, DigitalOcean Managed Databases, Heroku Postgres

## 🗃️ Database Management

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Backing Up Database

```bash
# PostgreSQL backup
pg_dump -U postgres service_marketplace > backup.sql

# Restore from backup
psql -U postgres service_marketplace < backup.sql
```

### Resetting Database

```bash
# Drop and recreate database
python manage.py flush

# Or completely reset
dropdb service_marketplace
createdb service_marketplace
python manage.py migrate
python manage.py createsuperuser
```

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'apps'`
- **Solution**: Ensure you're in the `backend` directory and virtual environment is activated

**Issue**: `django.db.utils.OperationalError: FATAL: database "service_marketplace" does not exist`
- **Solution**: Create the database using `createdb service_marketplace` or pgAdmin

**Issue**: `SMTP authentication error`
- **Solution**: 
  - For Gmail, use an App Password instead of your regular password
  - Ensure 2FA is enabled on your Google account
  - Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env

**Issue**: `OpenAI API error: Invalid API key`
- **Solution**: 
  - Verify your API key at https://platform.openai.com/api-keys
  - Ensure the key is correctly set in OPENAI_API_KEY
  - Check that you have credits in your OpenAI account

#### Frontend Issues

**Issue**: `Network Error` when calling API
- **Solution**: 
  - Ensure backend is running on http://localhost:8000
  - Check VITE_API_BASE_URL in frontend/.env
  - Verify CORS_ALLOWED_ORIGINS includes http://localhost:5173

**Issue**: `Module not found` errors
- **Solution**: Delete `node_modules` and `package-lock.json`, then run `npm install`

**Issue**: Build fails with TypeScript errors
- **Solution**: Run `npm run build` to see detailed errors, fix type issues

### Getting Help

- Check [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details
- Review API documentation in ARCHITECTURE.md
- Check browser console for frontend errors
- Check Django logs for backend errors

## 📦 Project Structure

```
service-marketplace-platform/
├── backend/                  # Django backend
│   ├── apps/                # Django applications
│   │   ├── users/          # User management
│   │   ├── services/       # Service management
│   │   ├── requests/       # Service requests
│   │   ├── problems/       # Problem reporting
│   │   └── analytics/      # Admin analytics
│   ├── config/             # Django configuration
│   ├── core/               # Shared utilities
│   ├── media/              # User uploads
│   ├── templates/          # Email templates
│   ├── tests/              # Integration tests
│   ├── manage.py           # Django CLI
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── lib/           # Utilities and API
│   │   ├── contexts/      # React contexts
│   │   ├── hooks/         # Custom hooks
│   │   ├── routes/        # Route configuration
│   │   └── types/         # TypeScript types
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite configuration
│   └── .env               # Environment variables
├── ARCHITECTURE.md        # Architecture documentation
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as a template
2. **Use strong SECRET_KEY** - Generate a new one for production
3. **Enable HTTPS in production** - Set SECURE_SSL_REDIRECT=True
4. **Rotate API keys regularly** - Especially OpenAI and email credentials
5. **Use environment-specific settings** - Separate dev/prod configurations
6. **Validate all user input** - Django serializers handle this automatically
7. **Keep dependencies updated** - Regularly run `pip list --outdated` and `npm outdated`

## 📄 API Documentation

For detailed API endpoint documentation, see the [API Endpoints section in ARCHITECTURE.md](./ARCHITECTURE.md#api-endpoints).

Quick reference:
- Authentication: `/api/users/`
- Services: `/api/services/`
- Requests: `/api/requests/`
- Problems: `/api/problems/`
- Analytics: `/api/analytics/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Development Team - Initial work

## 🙏 Acknowledgments

- Django REST Framework for the robust API framework
- React and Vite for the modern frontend tooling
- Radix UI and shadcn/ui for accessible components
- OpenAI for AI recommendation capabilities
- Framer Motion for smooth animations

---

**Version**: 1.0.0  
**Last Updated**: November 2024

For questions or support, please open an issue on GitHub.
#   S y r i a n - S e r v i c e  
 