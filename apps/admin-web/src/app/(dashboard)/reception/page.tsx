import { DashboardShell } from '@/features/dashboard/dashboard-shell';

export default function Page() {
  return <DashboardShell title="Reception Dashboard" description="Front-desk workflows for member onboarding, QR attendance, renewals, payment follow-up, and notifications." role="RECEPTION" metrics={[{ label: 'Walk-ins', value: '42', delta: 'Today', tone: 'blue' as const },{ label: 'Renewals', value: '29', delta: 'Due', tone: 'red' as const },{ label: 'Payments', value: 'INR 1.8L', delta: 'Collected', tone: 'green' as const },{ label: 'New Leads', value: '76', delta: '+14%', tone: 'gold' as const }]} focusAreas={['Check-in Desk','Renewal Queue','Payment Follow-up']} />;
}
