'use client';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import { endpoints } from '@/lib/api';
import { useAuth } from '@/stores/auth';
import { Button, Card, Input } from './ui';

export function ResourcePage({ resource, sample }: { resource: string; sample: Record<string, unknown> }) {
  const token = useAuth((s) => s.accessToken);
  const qc = useQueryClient();
  const [json, setJson] = useState(JSON.stringify(sample, null, 2));
  const query = useQuery({ queryKey: [resource, token], queryFn: () => endpoints.list<Record<string, unknown>>(resource, token), enabled: Boolean(token) });
  const mutation = useMutation({ mutationFn: () => endpoints.create(resource, JSON.parse(json), token), onSuccess: () => qc.invalidateQueries({ queryKey: [resource, token] }) });
  return <section className="space-y-6 p-8"><h2 className="text-4xl font-bold capitalize">{resource.replaceAll('-', ' ')}</h2><Card><textarea className="min-h-48 w-full rounded-xl bg-black/50 p-4 font-mono text-sm" value={json} onChange={(e) => setJson(e.target.value)} /><Button className="mt-4" onClick={() => mutation.mutate()}>Create</Button></Card><Card><h3 className="mb-4 text-xl font-semibold">Records</h3><pre className="overflow-auto text-sm text-zinc-300">{JSON.stringify(query.data ?? [], null, 2)}</pre></Card></section>;
}
