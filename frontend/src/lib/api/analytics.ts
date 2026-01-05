import apiClient from './axios';
import type { 
  DashboardMetrics, 
  UserStatistics, 
  RequestStatistics, 
  ProviderStatistics,
  AnalyticsFilters,
  ExportParams,
  PaginatedResponse
} from '@/types';

export const analyticsApi = {
  getDashboardMetrics: async (filters?: AnalyticsFilters) => {
    const response = await apiClient.get<DashboardMetrics>('/analytics/dashboard/', { params: filters });
    return response.data;
  },

  getUserStatistics: async (filters?: AnalyticsFilters) => {
    const response = await apiClient.get<UserStatistics[]>('/analytics/users/registrations/', { params: filters });
    return response.data;
  },

  getRequestStatistics: async (filters?: AnalyticsFilters) => {
    const response = await apiClient.get<RequestStatistics[]>('/analytics/requests/stats/', { params: filters });
    return response.data;
  },

  getProviderStatistics: async (filters?: AnalyticsFilters) => {
    const response = await apiClient.get<ProviderStatistics[]>('/analytics/providers/activity/', { params: filters });
    return response.data;
  },

  exportData: async (params: ExportParams) => {
    const response = await apiClient.get('/analytics/export/', { 
      params: {
        type: params.export_type,
        start_date: params.start_date,
        end_date: params.end_date,
        role: params.role,
        status: params.status,
      },
      responseType: 'blob'
    });
    return response.data;
  },

  search: async (query: string, type: 'users' | 'providers' | 'requests') => {
    let endpoint = '';
    switch (type) {
      case 'users':
        endpoint = '/analytics/users/search/';
        break;
      case 'providers':
        endpoint = '/analytics/providers/search/';
        break;
      case 'requests':
        endpoint = '/analytics/requests/search/';
        break;
    }
    const response = await apiClient.get<PaginatedResponse<any>>(endpoint, { 
      params: { q: query } 
    });
    return response.data;
  },
};
