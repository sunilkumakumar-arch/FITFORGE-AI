import { DashboardShell } from '@/features/dashboard/dashboard-shell';

export default function Page() {
  return <DashboardShell title="Trainer Dashboard" description="Assigned clients, programs, nutrition adherence, progress logs, messages, and posture review queues." role="TRAINER" metrics={[{ label: 'Clients', value: '64', delta: '+3', tone: 'gold' as const },{ label: 'Sessions Done', value: '218', delta: 'This week', tone: 'green' as const },{ label: 'Nutrition Logs', value: '74%', delta: '+8%', tone: 'blue' as const },{ label: 'Reviews Due', value: '11', delta: 'Today', tone: 'red' as const }]} focusAreas={['Client Progress','Program Builder','Posture Reviews']} />;
}
