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

  async forgotPassword(email: string): Promise<{ message: string }> {
    const res = await apiClient.post('/auth/forgot-password', { email });
    return res.data;
  },

  async resetPassword(email: string, code: string, new_password: string): Promise<{ message: string }> {
    const res = await apiClient.post('/auth/reset-password', { email, code, new_password });
    return res.data;
  },
};
