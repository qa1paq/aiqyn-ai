import apiClient from './client';
import { Gamification, Achievement } from '../types';

export const gamificationApi = {
  async getMyGamification(): Promise<Gamification> {
    const res = await apiClient.get('/gamification/me');
    return res.data;
  },

  async getAchievements(): Promise<Achievement[]> {
    const res = await apiClient.get('/gamification/achievements');
    return res.data;
  },

  async dailyCheckin() {
    const res = await apiClient.post('/gamification/daily-checkin');
    return res.data;
  },
};
