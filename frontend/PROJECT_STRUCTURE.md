# Frontend Project Structure

## Overview
This document describes the complete structure of the Service Marketplace Platform frontend application.

## Directory Structure

```
frontend/
├── public/                     # Static assets
├── src/
│   ├── components/            # React components
│   │   └── ui/               # shadcn/ui base components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── dialog.tsx
│   │       ├── input.tsx
│   │       ├── label.tsx
│   │       ├── toast.tsx
│   │       └── toaster.tsx
│   │
│   ├── hooks/                # Custom React hooks
│   │   └── use-toast.ts     # Toast notification hook
│   │
│   ├── lib/                  # Core utilities and configurations
│   │   ├── api/             # API client and service modules
│   │   │   ├── axios.ts     # Axios instance with interceptors
│   │   │   ├── auth.ts      # Authentication API calls
│   │   │   ├── services.ts  # Services API calls
│   │   │   ├── requests.ts  # Service requests API calls
│   │   │   ├── problems.ts  # Problem reports API calls
│   │   │   ├── analytics.ts # Analytics API calls
│   │   │   ├── providers.ts # Provider management API calls
│   │   │   └── index.ts     # API exports
│   │   │
│   │   ├── store/           # Zustand state management
│   │   │   ├── auth-store.ts # Authentication state
│   │   │   └── index.ts     # Store exports
│   │   │
│   │   ├── query-client.ts  # React Query configuration
│   │   └── utils.ts         # Utility functions (cn helper)
│   │
│   ├── routes/              # React Router configuration
│   │   └── index.tsx        # Route definitions and ProtectedRoute
│   │
│   ├── types/               # TypeScript type definitions
│   │   ├── user.ts          # User and auth types
│   │   ├── service.ts       # Service types
│   │   ├── request.ts       # Service request types
│   │   ├── problem.ts       # Problem report types
│   │   ├── analytics.ts     # Analytics types
│   │   └── index.ts         # Type exports
│   │
│   ├── App.tsx              # Root component
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles with Tailwind
│
├── .env                      # Environment variables
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── eslint.config.js         # ESLint configuration
├── index.html               # HTML template
├── package.json             # Dependencies and scripts
├── postcss.config.js        # PostCSS configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript base configuration
├── tsconfig.app.json        # TypeScript app configuration
├── tsconfig.node.json       # TypeScript node configuration
├── vite.config.ts           # Vite configuration
├── README.md                # Project documentation
└── PROJECT_STRUCTURE.md     # This file
```

## Key Files and Their Purpose

### Configuration Files

- **vite.config.ts**: Vite build tool configuration with path aliases
- **tailwind.config.js**: Tailwind CSS theme and plugin configuration
- **postcss.config.js**: PostCSS plugins configuration
- **tsconfig.*.json**: TypeScript compiler options
- **.env**: Environment variables (API URL, etc.)

### Core Application Files

- **src/main.tsx**: Application entry point, renders App component
- **src/App.tsx**: Root component with providers (QueryClient, Router, Toast)
- **src/index.css**: Global styles with Tailwind directives and CSS variables

### API Layer (src/lib/api/)

All API communication is centralized here:
- **axios.ts**: Configured Axios instance with JWT token interceptors
- **auth.ts**: Authentication endpoints (login, register, password change)
- **services.ts**: Service CRUD operations
- **requests.ts**: Service request management
- **problems.ts**: Problem reporting with AI recommendations
- **analytics.ts**: Admin analytics and reporting
- **providers.ts**: Provider application management

### State Management

- **src/lib/store/auth-store.ts**: Zustand store for authentication state
- **src/lib/query-client.ts**: React Query configuration for server state

### Routing (src/routes/)

- **index.tsx**: Route definitions with role-based protection
  - Landing page (/)
  - Login (/login)
  - Register (/register)
  - User dashboard (/dashboard/user)
  - Provider dashboard (/dashboard/provider)
  - Admin dashboard (/dashboard/admin)

### Type Definitions (src/types/)

TypeScript interfaces for all API models:
- User, ProviderProfile, AuthTokens
- Service, ServiceFormData, ServiceSearchParams
- ServiceRequest, RequestStatus
- ProblemReport, InputType
- DashboardMetrics, Analytics types
- PaginatedResponse, ApiError

### UI Components (src/components/ui/)

shadcn/ui components with Radix UI primitives:
- Button, Input, Label
- Card, Dialog
- Toast, Toaster

### Custom Hooks (src/hooks/)

- **use-toast.ts**: Toast notification management

## Technology Stack

### Core
- React 18+ with TypeScript
- Vite (build tool)
- React Router (navigation)

### Styling
- TailwindCSS (utility-first CSS)
- Radix UI (accessible primitives)
- shadcn/ui (pre-built components)
- Framer Motion (animations)

### State Management
- React Query (server state)
- Zustand (client state)

### HTTP Client
- Axios with interceptors

## Development Workflow

1. **Start dev server**: `npm run dev`
2. **Build for production**: `npm run build`
3. **Preview production build**: `npm run preview`
4. **Type check**: `npx tsc --noEmit`

## Environment Variables

Required environment variables in `.env`:
- `VITE_API_BASE_URL`: Backend API base URL

## Next Steps

The following components will be implemented in subsequent tasks:
- Landing page with animations
- Authentication pages (login, register)
- User dashboard components
- Provider dashboard components
- Admin dashboard components
- Shared layout components
