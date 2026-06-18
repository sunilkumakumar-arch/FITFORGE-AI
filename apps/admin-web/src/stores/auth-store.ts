import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type Role = 'super_admin' | 'branch_admin' | 'fitness_manager' | 'trainer' | 'receptionist' | 'member';

interface AuthState {
  accessToken?: string;
  refreshToken?: string;
  role: Role;
  setTokens: (accessToken: string, refreshToken: string) => void;
  setRole: (role: Role) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      role: 'super_admin',
      setTokens: (accessToken, refreshToken) => set({ accessToken, refreshToken }),
      setRole: (role) => set({ role }),
      logout: () => set({ accessToken: undefined, refreshToken: undefined }),
    }),
    { name: 'fitforge-admin-auth' },
  ),
);
