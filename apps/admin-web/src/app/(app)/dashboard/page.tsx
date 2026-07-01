'use client';

import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { BadgeCheck, Dumbbell, IndianRupee, Users } from 'lucide-react';
import { Card } from '@/components/ui';
import { endpoints, formatCurrency } from '@/lib/api';
import { useAuth } from '@/stores/auth';

function MetricCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string | number }) {
  return (
    <Card className="flex flex-col items-center justify-center gap-3 text-center">
      <div className="text-white/80">{icon}</div>
      <strong className="text-4xl font-black text-white">{value}</strong>
      <p className="text-sm uppercase tracking-wide text-zinc-400">{label}</p>
    </Card>
  );
}

export default function Dashboard() {
  const token = useAuth((s) => s.accessToken);
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard', token],
    queryFn: () => endpoints.dashboard(token),
    enabled: Boolean(token),
  });

  if (!token) {
    return (
      <section className="space-y-6 p-8">
        <h2 className="text-center text-5xl font-black">FITFORGE</h2>
        <Card className="text-center text-zinc-300">Please log in to view dashboard data.</Card>
      </section>
    );
  }

  if (isLoading) {
    return (
      <section className="space-y-6 p-8">
        <h2 className="text-center text-5xl font-black">FITFORGE</h2>
        <Card className="text-center text-zinc-300">Loading dashboard...</Card>
      </section>
    );
  }

  if (error) {
    return (
      <section className="space-y-6 p-8">
        <h2 className="text-center text-5xl font-black">FITFORGE</h2>
        <Card className="text-center text-red-300">Unable to load dashboard. Check that the API is running and you are logged in.</Card>
      </section>
    );
  }

  const plans = data?.membershipPlans ?? [];

  return (
    <section className="space-y-8 p-8">
      <h2 className="text-center text-5xl font-black">FITFORGE</h2>

      <div className="mx-auto grid max-w-4xl gap-4 md:grid-cols-2">
        <MetricCard icon={<Users size={32} />} label="Members" value={data?.members ?? 0} />
        <MetricCard icon={<Dumbbell size={32} />} label="Trainers" value={data?.trainers ?? 0} />
        <MetricCard icon={<IndianRupee size={32} />} label="Revenue" value={formatCurrency(data?.revenueMinor ?? 0, data?.currency)} />
        <MetricCard icon={<BadgeCheck size={32} />} label="Attendance" value={data?.attendance ?? 0} />
      </div>

      <div className="mx-auto max-w-4xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-bold">Membership Plans</h3>
          <Link className="text-sm text-yellow-400 hover:underline" href="/membership-plans">
            Manage plans
          </Link>
        </div>

        {plans.length === 0 ? (
          <Card className="text-center text-zinc-400">
            <p>No membership plans found.</p>
            <Link className="mt-3 inline-block text-yellow-400 hover:underline" href="/membership-plans">
              Create your first plan
            </Link>
          </Card>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {plans.map((plan) => (
              <Card key={plan.id}>
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h4 className="text-xl font-bold">{plan.name}</h4>
                    <p className="mt-1 text-zinc-400">{plan.durationDays} days</p>
                  </div>
                  <strong className="text-2xl text-yellow-400">{formatCurrency(plan.priceMinor, plan.currency)}</strong>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
