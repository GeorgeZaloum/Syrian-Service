import apiClient from './axios';
import type { ProviderProfile, User, PaginatedResponse } from '@/types';

export interface ProviderApplication extends ProviderProfile {
  user_details: User;
}

export const providersApi = {
  listApplications: async () => {
    const response = await apiClient.get<PaginatedResponse<ProviderApplication>>('/auth/providers/applications/');
    return response.data;
  },

  approve: async (id: number) => {
    const response = await apiClient.post<ProviderApplication>(`/auth/providers/applications/${id}/approve/`);
    return response.data;
  },

  reject: async (id: number) => {
    const response = await apiClient.post<ProviderApplication>(`/auth/providers/applications/${id}/reject/`);
    return response.data;
  },
};
