import { DashboardShell } from '@/features/dashboard/dashboard-shell';

export default function Page() {
  return <DashboardShell title="Branch Dashboard" description="Live branch operating center for attendance, memberships, renewals, stock, and local sales." role="BRANCH ADMIN" metrics={[{ label: 'Today Check-ins', value: '642', delta: '+9%', tone: 'green' as const },{ label: 'Active Members', value: '3,842', delta: '+4.2%', tone: 'gold' as const },{ label: 'Renewals Due', value: '86', delta: 'Today', tone: 'red' as const },{ label: 'Store Sales', value: 'INR 4.6L', delta: '+12%', tone: 'blue' as const }]} focusAreas={['Attendance Flow','Membership Renewals','Local Commerce']} />;
}
