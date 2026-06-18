import { DashboardShell } from '@/features/dashboard/dashboard-shell';

export default function Page() {
  return <DashboardShell title="Fitness Manager Dashboard" description="Programming, trainer performance, posture risk trends, workout completion, and member outcomes." role="FITNESS MANAGER" metrics={[{ label: 'Completion', value: '91%', delta: '+6%', tone: 'green' as const },{ label: 'Active Plans', value: '1,204', delta: '+88', tone: 'gold' as const },{ label: 'Risk Reduction', value: '22%', delta: '+5%', tone: 'blue' as const },{ label: 'Trainer Load', value: '38', delta: 'Balanced', tone: 'green' as const }]} focusAreas={['Trainer Quality','Workout Completion','Posture Risk']} />;
}
