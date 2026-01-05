import { createContext, useEffect, type ReactNode } from 'react';
import { useAuthStore } from '@/lib/store';
import { authApi } from '@/lib/api';
import type { User } from '@/types';

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<User>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const { user, setAuth, setUser, clearAuth, isAuthenticated } = useAuthStore();

  // Refresh user data on mount if authenticated
  useEffect(() => {
    const initAuth = async () => {
      if (isAuthenticated() && !user) {
        try {
          const userData = await authApi.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          clearAuth();
        }
      }
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const tokens = await authApi.login({ email, password });
    // Store tokens first so they're available for the next request
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    // Now fetch user data with the token in place
    const userData = await authApi.getCurrentUser();
    setAuth(userData, tokens.access, tokens.refresh);
    return userData;
  };

  const logout = () => {
    clearAuth();
  };

  const refreshUser = async () => {
    const userData = await authApi.getCurrentUser();
    setUser(userData);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: isAuthenticated(),
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
