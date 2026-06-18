import { Activity, Apple, BarChart3, Bell, Boxes, Building2, Camera, CreditCard, Dumbbell, LibraryBig, Package, Store, Users } from 'lucide-react';

export const dashboards = [
  { title: 'Super Admin', href: '/super-admin', description: 'Global tenants, revenue, compliance, and platform health.' },
  { title: 'Branch', href: '/branch', description: 'Branch operations, attendance, memberships, and local revenue.' },
  { title: 'Fitness Manager', href: '/fitness-manager', description: 'Programs, trainers, member outcomes, and posture insights.' },
  { title: 'Trainer', href: '/trainer', description: 'Assigned clients, workout plans, nutrition, and progress tracking.' },
  { title: 'Reception', href: '/reception', description: 'Front desk attendance, renewals, payments, and member onboarding.' },
] as const;

export const featureNav = [
  { title: 'Attendance', href: '/attendance', icon: Activity },
  { title: 'Memberships', href: '/memberships', icon: CreditCard },
  { title: 'Workout Programs', href: '/workouts', icon: Dumbbell },
  { title: 'Exercise Library', href: '/exercises', icon: LibraryBig },
  { title: 'Nutrition Plans', href: '/nutrition', icon: Apple },
  { title: 'Progress Tracking', href: '/progress', icon: BarChart3 },
  { title: 'AI Posture', href: '/posture', icon: Camera },
  { title: 'Inventory', href: '/inventory', icon: Boxes },
  { title: 'E-commerce Store', href: '/store', icon: Store },
  { title: 'Notifications', href: '/notifications', icon: Bell },
  { title: 'Reports', href: '/reports', icon: Package },
  { title: 'Organizations', href: '/organizations', icon: Building2 },
  { title: 'Users', href: '/users', icon: Users },
] as const;
