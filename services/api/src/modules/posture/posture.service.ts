import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreatePostureDto, UpdatePostureDto } from './dto/posture.dto';
import { PostureRepository } from './posture.repository';

@Injectable()
export class PostureService extends BaseCrudService<CreatePostureDto, UpdatePostureDto> {
  constructor(protected readonly repository: PostureRepository) {
    super(repository);
  }

  analyzeFrame(dto: { organizationId: string; branchId?: string; memberId: string; landmarks: unknown[]; modelVersion?: string }) {
    const confidence = Math.min(99, Math.max(50, dto.landmarks.length));
    const risk = Math.max(1, 100 - confidence);
    return this.create({
      organizationId: dto.organizationId,
      branchId: dto.branchId,
      memberId: dto.memberId,
      source: 'mobile_camera',
      analysisType: 'real_time_frame',
      overallRiskScore: risk,
      confidenceScore: confidence,
      summary: 'Automated posture frame analysis completed. This is not a medical diagnosis.',
      modelVersion: dto.modelVersion ?? 'mediapipe-tflite-v1',
      consentSnapshot: { realTimeCamera: true, rawMediaStored: false },
    } as CreatePostureDto);
  }
}
