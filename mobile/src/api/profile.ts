import apiClient from './client';
import { Profile } from '../types';

export const profileApi = {
  async getMyProfile(): Promise<Profile> {
    const res = await apiClient.get('/profile/me');
    return res.data;
  },

  async updateProfile(data: Partial<Profile>): Promise<Profile> {
    const res = await apiClient.put('/profile/me', data);
    return res.data;
  },
};
