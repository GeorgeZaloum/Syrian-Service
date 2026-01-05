export interface DashboardMetrics {
  total_users: number;
  total_regular_users: number;
  total_providers: number;
  active_providers: number;
  pending_applications: number;
  pending_requests: number;
  accepted_requests: number;
  completed_requests: number;
  rejected_requests: number;
  total_services: number;
}

export interface UserStatistics {
  date: string;
  count: number;
  role?: string;
}

export interface RequestStatistics {
  date: string;
  count: number;
  status?: string;
}

export interface ProviderStatistics {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
  services_count: number;
  received_requests_count: number;
  accepted_requests_count: number;
  completed_requests_count: number;
  provider_name?: string;
  total_requests?: number;
  accepted_requests?: number;
}

export interface AnalyticsFilters {
  start_date?: string;
  end_date?: string;
  role?: string;
  activity_type?: string;
}

export interface ExportParams extends AnalyticsFilters {
  export_type: 'users' | 'requests' | 'providers' | 'metrics';
  status?: string;
}
