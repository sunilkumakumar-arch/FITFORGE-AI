import { notFound } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { DataTable } from '@/components/ui/table';
import { featureCopy } from '@/lib/feature-data';

export function FeaturePage({ feature }: { feature: string }) {
  const copy = featureCopy[feature];
  if (!copy) notFound();

  return (
    <main className="space-y-6 p-6 lg:p-8">
      <section className="flex flex-col justify-between gap-4 rounded-[2rem] border border-yellow-500/20 bg-yellow-500/10 p-8 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-yellow-300">FITFORGE Module</p>
          <h1 className="mt-3 text-4xl font-bold">{copy.title}</h1>
          <p className="mt-3 max-w-3xl text-[var(--muted-foreground)]">{copy.description}</p>
        </div>
        <Button>{copy.cta}</Button>
      </section>
      <Card>
        <CardHeader>
          <CardTitle>Operational Records</CardTitle>
          <CardDescription>Representative API-ready records for this module. Wire to the NestJS backend endpoints as they are merged.</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable rows={copy.records} />
        </CardContent>
      </Card>
    </main>
  );
}
