import axios from 'axios';
import { tokenStorage } from '../storage/tokenStorage';

// Local:  'http://192.168.0.125:8000/api/v1'
// Cloud:  'https://YOUR-APP.up.railway.app/api/v1'
const BASE_URL = 'https://aiqyn-ai-production.up.railway.app/api/v1';

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use(async (config) => {
  const token = await tokenStorage.get();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.message ||
      'Something went wrong';
    return Promise.reject(new Error(message));
  }
);

export default apiClient;
