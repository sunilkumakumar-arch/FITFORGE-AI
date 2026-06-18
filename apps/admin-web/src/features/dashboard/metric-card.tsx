import { DashboardMetric } from '@/lib/api/types';
import { Card } from '@/components/ui/card';

const toneClasses: Record<DashboardMetric['tone'], string> = {
  gold: 'text-yellow-300',
  green: 'text-emerald-300',
  blue: 'text-sky-300',
  red: 'text-red-300',
};

export function MetricCard({ metric }: { metric: DashboardMetric }) {
  return (
    <Card className="p-5">
      <p className="text-sm text-[var(--muted-foreground)]">{metric.label}</p>
      <div className="mt-3 flex items-end justify-between gap-4">
        <strong className="text-3xl font-bold">{metric.value}</strong>
        <span className={toneClasses[metric.tone]}>{metric.delta}</span>
      </div>
    </Card>
  );
}
