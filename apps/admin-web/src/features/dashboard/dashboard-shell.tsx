import { DashboardMetric } from '@/lib/api/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MetricCard } from './metric-card';

interface DashboardShellProps {
  title: string;
  description: string;
  role: string;
  metrics: DashboardMetric[];
  focusAreas: string[];
}

export function DashboardShell({ title, description, role, metrics, focusAreas }: DashboardShellProps) {
  return (
    <main className="space-y-8 p-6 lg:p-8">
      <section className="rounded-[2rem] border border-yellow-500/20 bg-gradient-to-br from-yellow-500/15 via-white/5 to-transparent p-8">
        <Badge>{role}</Badge>
        <h1 className="mt-5 max-w-4xl text-4xl font-bold tracking-tight lg:text-6xl">{title}</h1>
        <p className="mt-4 max-w-3xl text-lg text-[var(--muted-foreground)]">{description}</p>
      </section>
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => <MetricCard key={metric.label} metric={metric} />)}
      </section>
      <section className="grid gap-4 xl:grid-cols-3">
        {focusAreas.map((area) => (
          <Card key={area}>
            <CardHeader>
              <CardTitle>{area}</CardTitle>
              <CardDescription>Operational controls, live status, API-backed workflows, and audit-ready actions.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-2 rounded-full bg-[var(--muted)]"><div className="h-2 w-3/4 rounded-full bg-yellow-500" /></div>
            </CardContent>
          </Card>
        ))}
      </section>
    </main>
  );
}
