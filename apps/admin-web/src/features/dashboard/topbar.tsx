'use client';

import { Bell, Moon, Search } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export function Topbar() {
  const { setTheme, theme } = useTheme();
  return (
    <header className="sticky top-0 z-10 flex items-center gap-3 border-b border-[var(--border)] bg-[var(--background)]/80 p-4 backdrop-blur">
      <div className="relative max-w-xl flex-1">
        <Search className="absolute left-3 top-3 size-4 text-[var(--muted-foreground)]" />
        <Input className="pl-10" placeholder="Search members, workouts, orders, reports..." />
      </div>
      <Button variant="outline" size="sm"><Bell size={16} /> Alerts</Button>
      <Button variant="ghost" size="sm" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}><Moon size={16} /></Button>
    </header>
  );
}
