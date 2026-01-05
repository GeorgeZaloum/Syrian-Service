import apiClient from './axios';
import type { 
  Service, 
  ServiceFormData, 
  ServiceSearchParams, 
  PaginatedResponse 
} from '@/types';

export const servicesApi = {
  list: async (params?: ServiceSearchParams) => {
    const response = await apiClient.get<PaginatedResponse<Service>>('/services/', { params });
    return response.data;
  },

  get: async (id: number) => {
    const response = await apiClient.get<Service>(`/services/${id}/`);
    return response.data;
  },

  create: async (data: ServiceFormData) => {
    const response = await apiClient.post<Service>('/services/', data);
    return response.data;
  },

  update: async (id: number, data: ServiceFormData) => {
    const response = await apiClient.put<Service>(`/services/${id}/`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/services/${id}/`);
  },
};
