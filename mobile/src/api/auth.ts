import apiClient from './client';
import { User } from '../types';

export const authApi = {
  async register(email: string, password: string, full_name: string): Promise<{ access_token: string }> {
    const res = await apiClient.post('/auth/register', { email, password, full_name });
    return res.data;
  },

  async login(email: string, password: string): Promise<{ access_token: string }> {
    const res = await apiClient.post('/auth/login', { email, password });
    return res.data;
  },

  async getMe(): Promise<User> {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },
};
