import { clsx } from 'clsx';
export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) { return <div className={clsx('rounded-3xl border border-white/10 bg-white/[.04] p-6 shadow-2xl shadow-black/20', className)} {...props} />; }
export function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement>) { return <button {...props} className={clsx('rounded-xl bg-yellow-500 px-4 py-2 font-semibold text-black disabled:opacity-60', props.className)} />; }
export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) { return <input {...props} className={clsx('w-full rounded-xl border border-white/10 bg-black/40 px-3 py-2 outline-none', props.className)} />; }
