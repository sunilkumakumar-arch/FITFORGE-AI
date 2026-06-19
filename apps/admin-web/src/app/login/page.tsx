'use client';
import { useState } from 'react';
import { endpoints } from '@/lib/api';
import { useAuth } from '@/stores/auth';
import { Button, Card, Input } from '@/components/ui';
export default function LoginPage() { const setTokens = useAuth((s) => s.setTokens); const [email,setEmail]=useState('admin@fitforge.ai'); const [password,setPassword]=useState('Fitforge@12345'); const [message,setMessage]=useState(''); async function login(){ try{ const t=await endpoints.login(email,password); setTokens(t.accessToken,t.refreshToken); setMessage('Logged in'); }catch{ setMessage('Backend unavailable or invalid credentials'); }} return <main className='grid min-h-screen place-items-center p-6'><Card className='w-full max-w-md'><h1 className='mb-6 text-3xl font-black'>FITFORGE AI Admin</h1><div className='space-y-3'><Input value={email} onChange={(e)=>setEmail(e.target.value)} /><Input type='password' value={password} onChange={(e)=>setPassword(e.target.value)} /><Button onClick={login}>Login</Button><p>{message}</p></div></Card></main> }
