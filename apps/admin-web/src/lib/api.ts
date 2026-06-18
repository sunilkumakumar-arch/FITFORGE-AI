const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:3000/api/v1';
export async function api<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}), ...init.headers } });
  if (!response.ok) throw new Error(`API ${response.status}`);
  return response.json() as Promise<T>;
}
export const endpoints = {
  login: (email: string, password: string) => api<{ accessToken: string; refreshToken: string }>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  list: <T>(resource: string, token?: string) => api<T[]>(`/${resource}`, {}, token),
  create: <T>(resource: string, body: unknown, token?: string) => api<T>(`/${resource}`, { method: 'POST', body: JSON.stringify(body) }, token),
  qrToken: (branchId: string, token?: string) => api<{ qrPayload: string; token: string; expiresAt: string }>('/attendance/qr-token', { method: 'POST', body: JSON.stringify({ branchId }) }, token),
  revenue: (token?: string) => api<{ revenueMinor: number; payments: number; currency: string }>('/analytics/revenue', {}, token),
  razorpayOrder: (body: unknown, token?: string) => api('/payments/razorpay/orders', { method: 'POST', body: JSON.stringify(body) }, token),
  whatsapp: (body: unknown, token?: string) => api('/whatsapp/send-template', { method: 'POST', body: JSON.stringify(body) }, token),
};
