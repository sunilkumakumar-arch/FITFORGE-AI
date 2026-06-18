import { PostureService } from './posture.service';

describe('PostureService', () => {
  it('creates a posture session result with scores and metrics', async () => {
    const prisma: any = { postureSession: { create: jest.fn().mockResolvedValue({ id: 'ps-1', organizationId: 'org-1', branchId: 'br-1' }) }, postureFinding: { create: jest.fn() } };
    const service = new PostureService(prisma, { log: jest.fn() } as any);
    const result = await service.analyzeFrame({ organizationId: 'org-1', branchId: 'br-1', memberId: 'mem-1', exerciseType: 'squat', landmarks: [
      { name: 'left_hip', x: 0, y: 0, visibility: 1 }, { name: 'left_knee', x: 0, y: 1, visibility: 1 }, { name: 'left_ankle', x: 1, y: 1, visibility: 1 },
      { name: 'right_hip', x: 0, y: 0, visibility: 1 }, { name: 'right_knee', x: 0, y: 1, visibility: 1 }, { name: 'right_ankle', x: -1, y: 1, visibility: 1 },
    ] });
    expect(result.sessionId).toBe('ps-1');
    expect(result.formScore).toBeGreaterThanOrEqual(0);
    expect(result.metrics.leftKnee).toBe(90);
  });
});
