import { Injectable } from '@nestjs/common';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';
import { AnalyzePostureFrameDto, CreateBodyMeasurementDto } from './dto/posture.dto';

type Landmark = { name: string; x: number; y: number; z?: number; visibility?: number };

@Injectable()
export class PostureService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}

  async analyzeFrame(dto: AnalyzePostureFrameDto, actorUserId?: string) {
    const metrics = this.calculateMetrics(dto.landmarks);
    const findings = this.generateFindings(dto.exerciseType, metrics);
    const averageConfidence = this.averageConfidence(dto.landmarks);
    const riskScore = Math.min(100, findings.reduce((sum, finding) => sum + (finding.severity === 'high' ? 30 : finding.severity === 'medium' ? 15 : 5), 0));
    const formScore = Math.max(0, 100 - riskScore);
    const session = await (this.prisma as any).postureSession.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, memberId: dto.memberId, capturedBy: dto.capturedBy, exerciseType: dto.exerciseType, overallRiskScore: riskScore, formScore, confidenceScore: averageConfidence, repCount: metrics.repCount ?? 0, summary: findings.length ? findings.map((finding) => finding.message).join(' ') : 'No major form issue detected.', metrics } });
    for (const finding of findings) await (this.prisma as any).postureFinding.create({ data: { postureSessionId: session.id, ...finding } });
    await this.audit.log({ action: 'posture.analyze_frame', entityType: 'postureSession', entityId: session.id, actorUserId, organizationId: session.organizationId, branchId: session.branchId, afterData: { riskScore, formScore, findings } });
    return { sessionId: session.id, riskScore, formScore, confidenceScore: averageConfidence, metrics, findings };
  }

  listSessions(query: any) { return (this.prisma as any).postureSession.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), ...(query.memberId ? { memberId: query.memberId } : {}) }, include: { findings: true }, orderBy: { createdAt: 'desc' } }); }

  createBodyMeasurement(dto: CreateBodyMeasurementDto) { const m = dto.measurements ?? {}; return (this.prisma as any).bodyMeasurement.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, memberId: dto.memberId, source: dto.source ?? 'manual', weightKg: m.weightKg, bodyFatPercent: m.bodyFatPercent, chestCm: m.chestCm, waistCm: m.waistCm, hipsCm: m.hipsCm } }); }

  private calculateMetrics(landmarks: Landmark[]) { const map = new Map(landmarks.map((l) => [l.name, l])); const angle = (a: string, b: string, c: string) => this.angle(map.get(a), map.get(b), map.get(c)); return { leftKnee: angle('left_hip','left_knee','left_ankle'), rightKnee: angle('right_hip','right_knee','right_ankle'), leftHip: angle('left_shoulder','left_hip','left_knee'), rightHip: angle('right_shoulder','right_hip','right_knee'), leftElbow: angle('left_shoulder','left_elbow','left_wrist'), rightElbow: angle('right_shoulder','right_elbow','right_wrist'), repCount: 0 }; }
  private generateFindings(exerciseType: string, metrics: any) { const findings: any[] = []; if (exerciseType === 'squat' && metrics.leftKnee && metrics.rightKnee && Math.abs(metrics.leftKnee - metrics.rightKnee) > 18) findings.push({ findingType: 'squat_asymmetry', severity: 'medium', confidenceScore: 82, message: 'Squat knee angles are asymmetric. Slow down and keep both knees tracking evenly.', correctivePlan: [{ name: 'tempo bodyweight squat', sets: 2, reps: 10 }] }); if (exerciseType === 'plank' && metrics.leftHip && metrics.leftHip < 145) findings.push({ findingType: 'plank_hip_sag', severity: 'medium', confidenceScore: 78, message: 'Plank hip angle suggests sagging. Brace glutes and ribs.', correctivePlan: [{ name: 'dead bug', sets: 2, reps: 8 }] }); return findings; }
  private angle(a?: Landmark, b?: Landmark, c?: Landmark) { if (!a || !b || !c) return null; const ab = { x: a.x - b.x, y: a.y - b.y }; const cb = { x: c.x - b.x, y: c.y - b.y }; const dot = ab.x * cb.x + ab.y * cb.y; const mag = Math.hypot(ab.x, ab.y) * Math.hypot(cb.x, cb.y); return mag ? Math.round((Math.acos(Math.max(-1, Math.min(1, dot / mag))) * 180 / Math.PI) * 10) / 10 : null; }
  private averageConfidence(landmarks: Landmark[]) { if (!landmarks.length) return 0; return Math.round((landmarks.reduce((sum, item) => sum + (item.visibility ?? 1), 0) / landmarks.length) * 1000) / 10; }
}
