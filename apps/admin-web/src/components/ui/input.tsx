import * as React from 'react';
import { cn } from '@/lib/utils';

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    className={cn('h-11 w-full rounded-xl border border-[var(--border)] bg-transparent px-4 text-sm outline-none transition placeholder:text-[var(--muted-foreground)] focus:ring-2 focus:ring-[var(--ring)]', className)}
    {...props}
  />
));
Input.displayName = 'Input';
