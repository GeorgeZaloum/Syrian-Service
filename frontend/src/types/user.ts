export type UserRole = 'REGULAR' | 'PROVIDER' | 'ADMIN';

export type ApprovalStatus = 'PENDING' | 'APPROVED' | 'REJECTED';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface ProviderProfile {
  id: number;
  user: number;
  service_description: string;
  approval_status: ApprovalStatus;
  approved_by: number | null;
  approved_at: string | null;
}

export interface RegisterUserData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  service_description?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface PasswordChangeData {
  current_password: string;
  new_password: string;
}
