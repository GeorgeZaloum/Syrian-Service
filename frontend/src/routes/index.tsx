import { createBrowserRouter } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { LoadingPage } from '@/components/layout';

// Lazy load pages for code splitting
const LandingPage = lazy(() => import('@/pages/LandingPage').then(m => ({ default: m.LandingPage })));
const LoginPage = lazy(() => import('@/pages/LoginPage').then(m => ({ default: m.LoginPage })));
const RegisterPage = lazy(() => import('@/pages/RegisterPage').then(m => ({ default: m.RegisterPage })));
const UserDashboard = lazy(() => import('@/pages/UserDashboard').then(m => ({ default: m.UserDashboard })));
const ProviderDashboard = lazy(() => import('@/pages/ProviderDashboard').then(m => ({ default: m.ProviderDashboard })));
const AdminDashboard = lazy(() => import('@/pages/AdminDashboard'));
const NotFoundPage = lazy(() => import('@/pages/NotFoundPage').then(m => ({ default: m.NotFoundPage })));
const ErrorPage = lazy(() => import('@/pages/ErrorPage').then(m => ({ default: m.ErrorPage })));

// Wrapper component for lazy loaded routes
const LazyRoute = ({ children }: { children: React.ReactNode }) => (
  <Suspense fallback={<LoadingPage />}>
    {children}
  </Suspense>
);

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <LazyRoute>
        <LandingPage />
      </LazyRoute>
    ),
    errorElement: (
      <LazyRoute>
        <ErrorPage />
      </LazyRoute>
    ),
  },
  {
    path: '/login',
    element: (
      <LazyRoute>
        <LoginPage />
      </LazyRoute>
    ),
    errorElement: (
      <LazyRoute>
        <ErrorPage />
      </LazyRoute>
    ),
  },
  {
    path: '/register',
    element: (
      <LazyRoute>
        <RegisterPage />
      </LazyRoute>
    ),
    errorElement: (
      <LazyRoute>
        <ErrorPage />
      </LazyRoute>
    ),
  },
  {
    path: '/dashboard/user',
    element: (
      <LazyRoute>
        <ProtectedRoute allowedRoles={['REGULAR']}>
          <UserDashboard />
        </ProtectedRoute>
      </LazyRoute>
    ),
    errorElement: (
      <LazyRoute>
        <ErrorPage />
      </LazyRoute>
    ),
  },
  {
    path: '/dashboard/provider',
    element: (
      <LazyRoute>
        <ProtectedRoute allowedRoles={['PROVIDER']}>
          <ProviderDashboard />
        </ProtectedRoute>
      </LazyRoute>
    ),
    errorElement: (
      <LazyRoute>
        <ErrorPage />
      </LazyRoute>
    ),
  },
  {
    path: '/dashboard/admin',
    element: (
      <LazyRoute>
        <ProtectedRoute allowedRoles={['ADMIN']}>
          <AdminDashboard />
        </ProtectedRoute>
      </LazyRoute>
    ),
    errorElement: (
      <LazyRoute>
        <ErrorPage />
      </LazyRoute>
    ),
  },
  {
    path: '*',
    element: (
      <LazyRoute>
        <NotFoundPage />
      </LazyRoute>
    ),
  },
]);
