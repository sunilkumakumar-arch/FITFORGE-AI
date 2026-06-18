import type { Metadata } from 'next';
import './globals.css';
import { AppProviders } from '@/components/providers/app-providers';

export const metadata: Metadata = {
  title: 'FITFORGE AI',
  description: 'Enterprise AI fitness ecosystem dashboard',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
