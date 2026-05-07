import apiClient from './client';
import { University, Major } from '../types';

export const universitiesApi = {
  async getUniversities(country?: string): Promise<University[]> {
    const params = country ? { country } : {};
    const res = await apiClient.get('/universities', { params });
    return res.data;
  },

  async getUniversity(id: number): Promise<University> {
    const res = await apiClient.get(`/universities/${id}`);
    return res.data;
  },

  async getRecommendedMajors(): Promise<Major[]> {
    const res = await apiClient.get('/majors/recommended');
    return res.data;
  },

  async chooseUniversity(university_id: number, major_id?: number): Promise<void> {
    await apiClient.post('/choices/university', {
      university_id,
      major_id: major_id ?? null,
      status: 'interested',
    });
  },

  async getMyChoices() {
    const res = await apiClient.get('/choices/me');
    return res.data;
  },
};
