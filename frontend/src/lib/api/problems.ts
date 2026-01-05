import apiClient from './axios';
import type { ProblemReport, CreateProblemReportData, PaginatedResponse } from '@/types';

export const problemsApi = {
  list: async () => {
    const response = await apiClient.get<PaginatedResponse<ProblemReport>>('/problems/');
    return response.data;
  },

  get: async (id: number) => {
    const response = await apiClient.get<ProblemReport>(`/problems/${id}/`);
    return response.data;
  },

  create: async (data: CreateProblemReportData) => {
    const formData = new FormData();
    formData.append('input_type', data.input_type);
    
    if (data.problem_text) {
      formData.append('problem_text', data.problem_text);
    }
    
    if (data.audio_file) {
      formData.append('audio_file', data.audio_file);
    }

    const response = await apiClient.post<ProblemReport>('/problems/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
