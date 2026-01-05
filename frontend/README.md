# Service Marketplace Platform - Frontend

Modern React frontend built with TypeScript, Vite, TailwindCSS, and shadcn/ui.

## Tech Stack

- **React 18+** with TypeScript
- **Vite** for fast development and building
- **TailwindCSS** for styling
- **Radix UI** for accessible component primitives
- **shadcn/ui** for pre-built components
- **Framer Motion** for animations
- **React Router** for navigation
- **React Query** for server state management
- **Zustand** for client state management
- **Axios** for HTTP requests

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Update `.env` with your backend API URL:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # React components
│   └── ui/             # shadcn/ui components
├── hooks/              # Custom React hooks
├── lib/                # Utilities and configurations
│   ├── api/           # API client and services
│   ├── store/         # Zustand stores
│   ├── query-client.ts # React Query configuration
│   └── utils.ts       # Utility functions
├── routes/            # React Router configuration
├── types/             # TypeScript type definitions
├── App.tsx            # Root component
├── main.tsx           # Entry point
└── index.css          # Global styles
```

## Features

- JWT authentication with automatic token refresh
- Role-based routing (Regular User, Service Provider, Admin)
- Type-safe API client with TypeScript
- Responsive design with TailwindCSS
- Toast notifications
- Optimistic updates with React Query
- Persistent auth state with Zustand

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: http://localhost:8000/api)
