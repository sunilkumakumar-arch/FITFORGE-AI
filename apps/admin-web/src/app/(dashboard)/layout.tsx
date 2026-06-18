import { Sidebar } from '@/features/dashboard/sidebar';
import { Topbar } from '@/features/dashboard/topbar';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="min-w-0 flex-1">
        <Topbar />
        {children}
      </div>
    </div>
  );
}
