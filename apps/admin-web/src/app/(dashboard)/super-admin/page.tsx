import { DashboardShell } from '@/features/dashboard/dashboard-shell';

export default function Page() {
  return <DashboardShell title="Super Admin Dashboard" description="Global control plane for tenants, branches, revenue, compliance, platform security, and AI usage." role="SUPER ADMIN" metrics={[{ label: 'Global MRR', value: 'INR 2.8Cr', delta: '+18.4%', tone: 'gold' as const },{ label: 'Active Branches', value: '128', delta: '+12', tone: 'green' as const },{ label: 'AI Scans', value: '84.2K', delta: '+31%', tone: 'blue' as const },{ label: 'Audit Alerts', value: '7', delta: '-4', tone: 'red' as const }]} focusAreas={['Tenant Governance','Revenue Intelligence','Security and Audit']} />;
}
