import apiClient from './axios';
import type { 
  ServiceRequest, 
  CreateServiceRequestData, 
  ServiceRequestListParams, 
  PaginatedResponse 
} from '@/types';

export const requestsApi = {
  list: async (params?: ServiceRequestListParams) => {
    const response = await apiClient.get<PaginatedResponse<ServiceRequest>>('/requests/', { params });
    return response.data;
  },

  get: async (id: number) => {
    const response = await apiClient.get<ServiceRequest>(`/requests/${id}/`);
    return response.data;
  },

  create: async (data: CreateServiceRequestData) => {
    const response = await apiClient.post<ServiceRequest>('/requests/', data);
    return response.data;
  },

  accept: async (id: number) => {
    const response = await apiClient.post<ServiceRequest>(`/requests/${id}/accept/`);
    return response.data;
  },

  reject: async (id: number) => {
    const response = await apiClient.post<ServiceRequest>(`/requests/${id}/reject/`);
    return response.data;
  },
};
