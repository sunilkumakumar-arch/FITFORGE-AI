const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:3000/api/v1';
export async function api<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}), ...init.headers } });
  if (!response.ok) throw new Error(`API ${response.status}`);
  return response.json() as Promise<T>;
}
export type MembershipPlan = {
  id: string;
  organizationId: string;
  branchId?: string | null;
  name: string;
  durationDays: number;
  priceMinor: number;
  currency: string;
  isActive: boolean;
};

export type DashboardStats = {
  members: number;
  trainers: number;
  revenueMinor: number;
  currency: string;
  attendance: number;
  membershipPlans: MembershipPlan[];
};

export const endpoints = {
  login: (email: string, password: string) => api<{ accessToken: string; refreshToken: string }>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  list: <T>(resource: string, token?: string) => api<T[]>(`/${resource}`, {}, token),
  create: <T>(resource: string, body: unknown, token?: string) => api<T>(`/${resource}`, { method: 'POST', body: JSON.stringify(body) }, token),
  dashboard: (token?: string) => api<DashboardStats>('/analytics/dashboard', {}, token),
  membershipPlans: (token?: string) => api<MembershipPlan[]>('/membership-plans', {}, token),
  qrToken: (branchId: string, token?: string) => api<{ qrPayload: string; token: string; expiresAt: string }>('/attendance/qr-token', { method: 'POST', body: JSON.stringify({ branchId }) }, token),
  revenue: (token?: string) => api<{ revenueMinor: number; payments: number; currency: string }>('/analytics/revenue', {}, token),
  razorpayOrder: (body: unknown, token?: string) => api('/payments/razorpay/orders', { method: 'POST', body: JSON.stringify(body) }, token),
  whatsapp: (body: unknown, token?: string) => api('/whatsapp/send-template', { method: 'POST', body: JSON.stringify(body) }, token),
};

export function formatCurrency(minor: number, currency = 'INR') {
  const major = minor / 100;
  if (currency === 'INR') return `₹${major.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
  return `${currency} ${major.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}
