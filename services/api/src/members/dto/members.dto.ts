import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class MemberDetailsDto {
  @ApiProperty() id!: string;
  @ApiProperty() email!: string;
  @ApiPropertyOptional() phone?: string | null;
  @ApiProperty() firstName!: string;
  @ApiProperty() lastName!: string;
  @ApiProperty() status!: string;
}

export class MembershipSummaryDto {
  @ApiPropertyOptional() planName?: string | null;
  @ApiPropertyOptional() status?: string | null;
  @ApiPropertyOptional() expiry?: string | null;
  @ApiPropertyOptional() remainingDays?: number | null;
}

export class TrainerSummaryDto {
  @ApiPropertyOptional() id?: string | null;
  @ApiPropertyOptional() firstName?: string | null;
  @ApiPropertyOptional() lastName?: string | null;
}

export class PtPackageSummaryDto {
  @ApiPropertyOptional() name?: string | null;
  @ApiPropertyOptional() expiry?: string | null;
  @ApiPropertyOptional() remainingSessions?: number | null;
}

export class MemberSummaryResponseDto {
  @ApiProperty({ type: MemberDetailsDto }) member!: MemberDetailsDto;
  @ApiProperty({ type: MembershipSummaryDto }) membership!: MembershipSummaryDto;
  @ApiProperty({ type: TrainerSummaryDto }) trainer!: TrainerSummaryDto;
  @ApiProperty({ type: PtPackageSummaryDto }) ptPackage!: PtPackageSummaryDto;
}
