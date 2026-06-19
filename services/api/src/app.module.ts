import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { APP_GUARD } from '@nestjs/core';
import { JwtModule } from '@nestjs/jwt';
import { AuthGuard } from './auth/auth.guard';
import { AuthController } from './auth/auth.controller';
import { AuthService } from './auth/auth.service';
import { RbacGuard } from './auth/rbac.guard';
import { RateLimitGuard } from './auth/rate-limit.guard';
import { PrismaService } from './core/prisma.service';
import { AuditService } from './core/audit.service';
import { ResourceController } from './resources/resource.controller';
import { ResourceService } from './resources/resource.service';
import { AttendanceController } from './attendance/attendance.controller';
import { AttendanceService } from './attendance/attendance.service';
import { PaymentsController } from './payments/payments.controller';
import { PaymentsService } from './payments/payments.service';
import { WhatsappController } from './whatsapp/whatsapp.controller';
import { WhatsappService } from './whatsapp/whatsapp.service';
import { AnalyticsController } from './analytics/analytics.controller';
import { MembershipsController } from './memberships/memberships.controller';
import { MembershipsService } from './memberships/memberships.service';
import { WorkoutsController } from './workouts/workouts.controller';
import { WorkoutsService } from './workouts/workouts.service';
import { NutritionController } from './nutrition/nutrition.controller';
import { NutritionService } from './nutrition/nutrition.service';
import { CommerceController } from './commerce/commerce.controller';
import { CommerceService } from './commerce/commerce.service';
import { TrainersController } from './trainers/trainers.controller';
import { TrainersService } from './trainers/trainers.service';
import { PostureController } from './posture/posture.controller';
import { PostureService } from './posture/posture.service';
import { JobsController } from './jobs/jobs.controller';
import { JobsService } from './jobs/jobs.service';
import { PtController } from './pt/pt.controller';
import { PtService } from './pt/pt.service';

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true, envFilePath: ['.env', '.env.example'] }), JwtModule.register({})],
  controllers: [
    AuthController,
    MembershipsController,
    AttendanceController,
    WorkoutsController,
    NutritionController,
    CommerceController,
    TrainersController,
    PostureController,
    JobsController,
    PtController,
    PaymentsController,
    WhatsappController,
    AnalyticsController,
    ResourceController,
  ],
  providers: [
    PrismaService,
    AuditService,
    AuthService,
    ResourceService,
    MembershipsService,
    AttendanceService,
    WorkoutsService,
    NutritionService,
    CommerceService,
    TrainersService,
    PostureService,
    JobsService,
    PtService,
    PaymentsService,
    WhatsappService,
    { provide: APP_GUARD, useClass: AuthGuard },
    { provide: APP_GUARD, useClass: RbacGuard },
    { provide: APP_GUARD, useClass: RateLimitGuard },
  ],
})
export class AppModule {}
