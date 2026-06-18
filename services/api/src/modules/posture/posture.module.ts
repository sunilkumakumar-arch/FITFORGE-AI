import { Module } from '@nestjs/common';
import { PostureController } from './posture.controller';
import { PostureRepository } from './posture.repository';
import { PostureService } from './posture.service';

@Module({
  controllers: [PostureController],
  providers: [PostureService, PostureRepository],
  exports: [PostureService],
})
export class PostureModule {}
