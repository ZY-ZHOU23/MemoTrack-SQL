import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const auth = {
  login: (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    return api.post('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },
  register: (email: string, username: string, password: string) =>
    api.post('/api/v1/auth/register', { email, username, password }),
  getCurrentUser: () => api.get('/api/v1/users/me'),
};

// Entries endpoints
export const entries = {
  getAll: () => api.get('/api/v1/entries'),
  getById: (id: number) => api.get(`/api/v1/entries/${id}`),
  create: (data: {
    title: string;
    content: string;
    category_id: number;
    priority?: string;
    status?: string;
    tags?: string[];
  }) => api.post('/api/v1/entries', data),
  update: (id: number, data: {
    title?: string;
    content?: string;
    category_id?: number;
    priority?: string;
    status?: string;
    tags?: string[];
  }) => api.put(`/api/v1/entries/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/entries/${id}`),
};

// Categories endpoints
export const categories = {
  getAll: () => api.get('/api/v1/categories'),
  getById: (id: number) => api.get(`/api/v1/categories/${id}`),
  create: (data: { name: string; description: string }) =>
    api.post('/api/v1/categories', data),
  update: (id: number, data: { name: string; description: string }) =>
    api.put(`/api/v1/categories/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/categories/${id}`),
};

// Tags endpoints
export const tags = {
  getAll: () => api.get('/api/v1/tags'),
  getById: (id: number) => api.get(`/api/v1/tags/${id}`),
  create: (data: { name: string }) => api.post('/api/v1/tags', data),
  update: (id: number, data: { name: string }) =>
    api.put(`/api/v1/tags/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/tags/${id}`),
};

// Analytics endpoints
export const analytics = {
  getDashboard: () => api.get('/api/v1/analytics/dashboard'),
  getAnalytics: (timeRange: string) =>
    api.get(`/api/v1/analytics?time_range=${timeRange}`),
};

export default api; 