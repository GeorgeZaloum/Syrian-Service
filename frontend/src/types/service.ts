export interface Service {
  id: number;
  provider: number;
  name: string;
  description: string;
  location: string;
  cost: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ServiceFormData {
  name: string;
  description: string;
  location: string;
  cost: string;
}

export interface ServiceSearchParams {
  search?: string;
  location?: string;
  min_cost?: number;
  max_cost?: number;
  page?: number;
}
