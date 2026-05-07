import apiClient from './client';
import { Roadmap } from '../types';

export const roadmapApi = {
  async generate(target_major: string, target_country: string): Promise<Roadmap> {
    const res = await apiClient.post('/roadmap/generate', { target_major, target_country });
    return res.data;
  },

  async getMyRoadmap(): Promise<Roadmap> {
    const res = await apiClient.get('/roadmap/me');
    return res.data;
  },

  async completeStep(step_id: number) {
    const res = await apiClient.post(`/roadmap/steps/${step_id}/complete`);
    return res.data;
  },

  async getDailyTasks() {
    const res = await apiClient.get('/roadmap/daily-tasks');
    return res.data;
  },
};
