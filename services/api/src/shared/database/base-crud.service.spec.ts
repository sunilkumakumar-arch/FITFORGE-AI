import { NotFoundException } from '@nestjs/common';
import { BaseCrudService } from './base-crud.service';

describe('BaseCrudService', () => {
  const repository = {
    create: jest.fn(),
    findMany: jest.fn(),
    count: jest.fn(),
    findById: jest.fn(),
    update: jest.fn(),
    softDelete: jest.fn(),
  };
  const service = new BaseCrudService(repository as any);

  beforeEach(() => jest.clearAllMocks());

  it('returns paginated results', async () => {
    repository.findMany.mockResolvedValue([{ id: '1' }]);
    repository.count.mockResolvedValue(1);
    await expect(service.findAll({ page: 1, limit: 25 })).resolves.toEqual({ items: [{ id: '1' }], total: 1, page: 1, limit: 25 });
  });

  it('throws when a resource is missing', async () => {
    repository.findById.mockResolvedValue(null);
    await expect(service.findOne('missing')).rejects.toBeInstanceOf(NotFoundException);
  });
});
