import { ResourcePage } from '@/components/resource-page';

export default function Page() {
  return (
    <ResourcePage
      resource="membership-plans"
      sample={{
        organizationId: '00000000-0000-0000-0000-000000000001',
        branchId: '00000000-0000-0000-0000-000000000002',
        name: 'Monthly Plan',
        durationDays: 30,
        priceMinor: 299900,
        currency: 'INR',
        isActive: true,
      }}
    />
  );
}
