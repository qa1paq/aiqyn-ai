import apiClient from './client';
import { AssessmentQuestion, AssessmentResult } from '../types';

export const assessmentApi = {
  async getQuestions(lang: string = 'ru'): Promise<AssessmentQuestion[]> {
    const res = await apiClient.get('/assessment/questions', { params: { lang } });
    return res.data;
  },

  async submitAnswers(answers: Record<string, string>, lang: string = 'ru'): Promise<AssessmentResult> {
    const res = await apiClient.post('/assessment/submit', { answers }, { params: { lang } });
    return res.data;
  },

  async getResult(): Promise<AssessmentResult> {
    const res = await apiClient.get('/assessment/result');
    return res.data;
  },
};
