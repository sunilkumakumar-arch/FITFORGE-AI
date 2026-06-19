import { create } from 'zustand';
type AuthState = { accessToken?: string; refreshToken?: string; setTokens: (a: string, r: string) => void; logout: () => void };
export const useAuth = create<AuthState>((set) => ({ setTokens: (accessToken, refreshToken) => set({ accessToken, refreshToken }), logout: () => set({ accessToken: undefined, refreshToken: undefined }) }));
