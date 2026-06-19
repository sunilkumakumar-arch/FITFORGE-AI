import { ResourceService } from './resource.service';

describe('ResourceService', () => {
  it('rejects unsupported resources', () => {
    const service = new ResourceService({} as any, {} as any);
    expect(() => service.meta('unknown')).toThrow('Unsupported resource');
  });
});
