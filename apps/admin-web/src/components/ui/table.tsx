import { cn } from '@/lib/utils';

export function DataTable({ rows }: { rows: Array<{ id: string; title: string; subtitle: string; status: string; metadata: string }> }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-[var(--border)]">
      <table className="w-full text-left text-sm">
        <thead className="bg-[var(--muted)] text-[var(--muted-foreground)]">
          <tr>
            <th className="px-4 py-3 font-medium">Name</th>
            <th className="px-4 py-3 font-medium">Scope</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Metric</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-t border-[var(--border)]">
              <td className="px-4 py-4 font-medium">{row.title}</td>
              <td className="px-4 py-4 text-[var(--muted-foreground)]">{row.subtitle}</td>
              <td className="px-4 py-4"><span className={cn('rounded-full bg-yellow-500/10 px-2.5 py-1 text-xs text-yellow-300')}>{row.status}</span></td>
              <td className="px-4 py-4 text-[var(--muted-foreground)]">{row.metadata}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
