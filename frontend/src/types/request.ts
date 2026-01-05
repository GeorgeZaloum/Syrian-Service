export type RequestStatus = 'PENDING' | 'ACCEPTED' | 'REJECTED' | 'COMPLETED';

export interface ServiceRequest {
  id: number;
  service: number;
  requester: number;
  provider: number;
  status: RequestStatus;
  message: string;
  created_at: string;
  updated_at: string;
}

export interface CreateServiceRequestData {
  service: number;
  message?: string;
}

export interface ServiceRequestListParams {
  status?: RequestStatus;
  page?: number;
}
