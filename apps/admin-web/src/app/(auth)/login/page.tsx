'use client';

import { useMutation } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { authApi } from '@/lib/api/client';
import { useAuthStore } from '@/stores/auth-store';

export default function LoginPage() {
  const router = useRouter();
  const setTokens = useAuthStore((state) => state.setTokens);
  const [email, setEmail] = useState('admin@fitforge.ai');
  const [password, setPassword] = useState('Fitforge@12345');
  const mutation = useMutation({
    mutationFn: () => authApi.login(email, password),
    onSuccess: (tokens) => {
      setTokens(tokens.accessToken, tokens.refreshToken);
      router.push('/super-admin');
    },
  });

  return (
    <main className="grid min-h-screen place-items-center p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-3xl">Welcome to FITFORGE AI</CardTitle>
          <CardDescription>Sign in to the enterprise fitness command center.</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={(event) => { event.preventDefault(); mutation.mutate(); }}>
            <Input value={email} onChange={(event) => setEmail(event.target.value)} type="email" placeholder="Email" />
            <Input value={password} onChange={(event) => setPassword(event.target.value)} type="password" placeholder="Password" />
            {mutation.error ? <p className="text-sm text-red-300">Unable to sign in. Check API availability and credentials.</p> : null}
            <Button className="w-full" disabled={mutation.isPending}>{mutation.isPending ? 'Signing in...' : 'Sign in'}</Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
