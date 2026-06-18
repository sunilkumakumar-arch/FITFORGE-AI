import Link from 'next/link';
import { Dumbbell } from 'lucide-react';
import { dashboards, featureNav } from '@/lib/navigation';

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-72 shrink-0 border-r border-[var(--border)] bg-black/30 p-6 backdrop-blur lg:block">
      <Link href="/super-admin" className="mb-10 flex items-center gap-3">
        <span className="grid size-11 place-items-center rounded-2xl bg-yellow-500 text-black"><Dumbbell size={22} /></span>
        <span>
          <strong className="block text-lg">FITFORGE AI</strong>
          <small className="text-[var(--muted-foreground)]">Enterprise Console</small>
        </span>
      </Link>
      <nav className="space-y-7">
        <div>
          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--muted-foreground)]">Dashboards</p>
          <div className="space-y-1">
            {dashboards.map((item) => <Link key={item.href} href={item.href} className="block rounded-xl px-3 py-2 text-sm hover:bg-white/10">{item.title}</Link>)}
          </div>
        </div>
        <div>
          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--muted-foreground)]">Operations</p>
          <div className="space-y-1">
            {featureNav.map((item) => <Link key={item.href} href={item.href} className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm hover:bg-white/10"><item.icon size={16} />{item.title}</Link>)}
          </div>
        </div>
      </nav>
    </aside>
  );
}
