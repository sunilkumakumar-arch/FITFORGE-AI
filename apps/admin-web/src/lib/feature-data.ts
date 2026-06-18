import { FeatureRecord } from './api/types';

export const featureCopy: Record<string, { title: string; description: string; cta: string; records: FeatureRecord[] }> = {
  attendance: {
    title: 'Attendance Tracking',
    description: 'QR, biometric, mobile, and manual attendance workflows for every branch.',
    cta: 'Record check-in',
    records: [
      { id: 'att-1', title: 'Morning peak', subtitle: 'Koramangala Branch', status: 'Live', metadata: '247 check-ins today' },
      { id: 'att-2', title: 'Biometric sync', subtitle: 'Reception terminal', status: 'Healthy', metadata: '2 min ago' },
    ],
  },
  memberships: {
    title: 'Memberships and Renewals',
    description: 'Plan assignment, renewal workflows, pause/cancel controls, and billing visibility.',
    cta: 'Create membership',
    records: [
      { id: 'mem-1', title: 'Elite Annual', subtitle: 'Renewal queue', status: 'Due soon', metadata: '38 members' },
      { id: 'mem-2', title: 'Branch Growth', subtitle: 'Monthly plan', status: 'Active', metadata: '812 members' },
    ],
  },
  workouts: {
    title: 'Workout Programs',
    description: 'Structured fat loss, strength, hypertrophy, powerlifting, and sports performance plans.',
    cta: 'Build program',
    records: [
      { id: 'wrk-1', title: '12-week hypertrophy', subtitle: 'Trainer assigned', status: 'Active', metadata: '156 clients' },
      { id: 'wrk-2', title: 'Powerlifting peak', subtitle: 'Advanced cohort', status: 'Draft', metadata: '4 days/week' },
    ],
  },
  exercises: {
    title: 'Exercise Library',
    description: 'Premium exercise database with safety instructions, coaching cues, images, and videos.',
    cta: 'Add exercise',
    records: [
      { id: 'ex-1', title: 'Barbell back squat', subtitle: 'Lower body', status: 'Published', metadata: 'Advanced' },
      { id: 'ex-2', title: 'Cable row', subtitle: 'Back', status: 'Published', metadata: 'Intermediate' },
    ],
  },
  nutrition: {
    title: 'Nutrition Plans',
    description: 'Macro targets, meal templates, allergy-aware recommendations, and adherence tracking.',
    cta: 'Create plan',
    records: [
      { id: 'nut-1', title: 'Fat loss macros', subtitle: 'High protein', status: 'Active', metadata: '1,850 kcal' },
      { id: 'nut-2', title: 'Muscle gain plan', subtitle: 'Vegetarian', status: 'Review', metadata: '2,750 kcal' },
    ],
  },
  progress: {
    title: 'Progress Tracking',
    description: 'Body metrics, strength trends, adherence, posture improvements, and transformation notes.',
    cta: 'Log progress',
    records: [
      { id: 'prg-1', title: 'Transformation cohort', subtitle: '90-day challenge', status: 'Improving', metadata: '+18% adherence' },
      { id: 'prg-2', title: 'Strength trend', subtitle: 'Trainer clients', status: 'On track', metadata: '+12% volume' },
    ],
  },
  posture: {
    title: 'AI Posture Analysis',
    description: 'Real-time camera posture capture, risk scoring, corrective exercise plans, and reports.',
    cta: 'Start scan',
    records: [
      { id: 'pos-1', title: 'Knee valgus scan', subtitle: 'Squat analysis', status: 'Medium risk', metadata: '82% confidence' },
      { id: 'pos-2', title: 'Forward head posture', subtitle: 'Static assessment', status: 'Low risk', metadata: '91% confidence' },
    ],
  },
  inventory: {
    title: 'Inventory Management',
    description: 'Supplements, apparel, equipment, barcode operations, stock alerts, and adjustments.',
    cta: 'Adjust stock',
    records: [
      { id: 'inv-1', title: 'Whey isolate', subtitle: 'Supplement shelf', status: 'Low stock', metadata: '8 units' },
      { id: 'inv-2', title: 'Lifting straps', subtitle: 'Accessories', status: 'Healthy', metadata: '164 units' },
    ],
  },
  store: {
    title: 'E-commerce Store',
    description: 'Premium marketplace for apparel, footwear, accessories, equipment, and supplements.',
    cta: 'Add product',
    records: [
      { id: 'ord-1', title: 'Gold performance tee', subtitle: 'Apparel', status: 'Trending', metadata: '4.8 rating' },
      { id: 'ord-2', title: 'Pre-workout stack', subtitle: 'Supplements', status: 'In stock', metadata: '312 sold' },
    ],
  },
  notifications: {
    title: 'Notifications',
    description: 'In-app, push, email, and SMS campaigns for renewals, workouts, payments, and alerts.',
    cta: 'Send campaign',
    records: [
      { id: 'not-1', title: 'Renewal reminder', subtitle: 'Reception workflow', status: 'Scheduled', metadata: 'Today 6 PM' },
      { id: 'not-2', title: 'Workout nudge', subtitle: 'Member engagement', status: 'Sent', metadata: '86% delivered' },
    ],
  },
  reports: {
    title: 'Reports and Analytics',
    description: 'Revenue, retention, attendance, trainer performance, sales, and AI posture insights.',
    cta: 'Export report',
    records: [
      { id: 'rep-1', title: 'Monthly revenue', subtitle: 'All branches', status: 'Ready', metadata: 'INR 48.2L' },
      { id: 'rep-2', title: 'Trainer performance', subtitle: 'Fitness manager', status: 'Ready', metadata: '94% completion' },
    ],
  },
  organizations: {
    title: 'Organization Management',
    description: 'Tenant, franchise, and branch hierarchy controls for enterprise deployments.',
    cta: 'Add organization',
    records: [
      { id: 'org-1', title: 'FITFORGE Elite', subtitle: 'Franchise tenant', status: 'Active', metadata: '18 branches' },
      { id: 'org-2', title: 'Downtown Strength', subtitle: 'Single gym', status: 'Active', metadata: '1 branch' },
    ],
  },
  users: {
    title: 'User Management',
    description: 'Admins, managers, trainers, receptionists, and members with branch-scoped RBAC.',
    cta: 'Invite user',
    records: [
      { id: 'usr-1', title: 'Trainer onboarding', subtitle: 'North branch', status: 'Pending', metadata: '6 invites' },
      { id: 'usr-2', title: 'Member imports', subtitle: 'Migration batch', status: 'Complete', metadata: '2,410 users' },
    ],
  },
};
