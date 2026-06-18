import type { Config } from 'jest';
const config: Config = { rootDir: '.', testRegex: '.*\.spec\.ts$', transform: { '^.+\.(t|j)s$': ['ts-jest', { tsconfig: 'tsconfig.json' }] }, testEnvironment: 'node' };
export default config;
