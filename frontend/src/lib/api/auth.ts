import apiClient from './axios';
import type { 
  User, 
  RegisterUserData, 
  LoginCredentials, 
  AuthTokens, 
  PasswordChangeData 
} from '@/types';

export const authApi = {
  register: async (data: RegisterUserData) => {
    const response = await apiClient.post<User>('/auth/register/', data);
    return response.data;
  },

  login: async (credentials: LoginCredentials) => {
    const response = await apiClient.post<{ tokens: AuthTokens }>('/auth/login/', credentials);
    return response.data.tokens;
  },

  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post<{ access: string }>('/auth/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await apiClient.get<User>('/auth/me/');
    return response.data;
  },

  changePassword: async (data: PasswordChangeData) => {
    const response = await apiClient.post('/auth/password/change/', data);
    return response.data;
  },
};
