export interface ApiListResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  tokenType: 'Bearer';
  expiresIn: string;
}

export interface DashboardMetric {
  label: string;
  value: string;
  delta: string;
  tone: 'gold' | 'green' | 'blue' | 'red';
}

export interface FeatureRecord {
  id: string;
  title: string;
  subtitle: string;
  status: string;
  metadata: string;
}
