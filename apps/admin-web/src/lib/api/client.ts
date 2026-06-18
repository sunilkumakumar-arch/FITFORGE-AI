import { AuthTokens } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:3000/api/v1';

export class ApiError extends Error {
  constructor(message: string, readonly status: number, readonly payload?: unknown) {
    super(message);
  }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'content-type': 'application/json',
      ...(token ? { authorization: `Bearer ${token}` } : {}),
      ...init.headers,
    },
  });

  const payload = response.headers.get('content-type')?.includes('application/json') ? await response.json() : undefined;
  if (!response.ok) {
    throw new ApiError(payload?.message ?? 'API request failed', response.status, payload);
  }
  return payload as T;
}

export const authApi = {
  login: (email: string, password: string) =>
    apiRequest<AuthTokens>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  me: (token: string) => apiRequest('/auth/me', {}, token),
};
