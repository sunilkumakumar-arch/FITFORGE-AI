import { NutritionService } from './nutrition.service';

describe('NutritionService', () => {
  it('calculates macro targets for fat loss', () => {
    const service = new NutritionService({} as any, {} as any);
    const result = service.calculateMacros({ weightKg: 80, heightCm: 178, age: 30, sex: 'male', goal: 'fat_loss' });
    expect(result.calories).toBeGreaterThan(1500);
    expect(result.proteinGrams).toBe(160);
    expect(result.carbsGrams).toBeGreaterThan(0);
    expect(result.fatGrams).toBeGreaterThan(0);
  });
});
