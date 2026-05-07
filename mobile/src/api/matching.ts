import apiClient from './client';
import { MatchUser } from '../types';

export const matchingApi = {
  async getFeed(limit = 20): Promise<MatchUser[]> {
    const res = await apiClient.get('/matching/feed', { params: { limit } });
    return res.data;
  },

  async performAction(target_user_id: number, action: 'like' | 'skip') {
    const res = await apiClient.post('/matching/action', { target_user_id, action });
    return res.data;
  },
};
