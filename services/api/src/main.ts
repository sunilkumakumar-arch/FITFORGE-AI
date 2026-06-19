import { ValidationPipe } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import helmet from 'helmet';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const config = app.get(ConfigService);
  app.use(helmet());
  app.enableCors({ origin: true, credentials: true });
  app.setGlobalPrefix('api/v1');
  app.useGlobalPipes(new ValidationPipe({ whitelist: false, transform: true }));
  const swagger = new DocumentBuilder().setTitle('FITFORGE AI API').setVersion('1.0.0').addBearerAuth().build();
  SwaggerModule.setup('docs', app, SwaggerModule.createDocument(app, swagger));
  await app.listen(config.get<number>('PORT') ?? 3000);
}
void bootstrap();
