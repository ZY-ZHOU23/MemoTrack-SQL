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
  console.log('API Request to:', config.url, 'Token exists:', !!token);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('Authorization header set');
  } else {
    console.log('No token found in localStorage');
  }
  return config;
});

// Add response error interceptor for auth errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      console.log('API Error:', error.response.status, error.response.data);
      
      // Handle auth errors
      if (error.response.status === 401 || error.response.status === 403) {
        console.error('Authentication error detected');
        
        // Check token status
        const token = localStorage.getItem('token');
        if (!token) {
          console.error('Token missing from localStorage');
        } else {
          console.error('Token exists but not valid:', token.substring(0, 20) + '...');
        }
      }
    }
    return Promise.reject(error);
  }
);

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
    category_id?: number;
    priority?: string;
    status?: string;
    tags?: string[];
    created_at?: string;
    metrics?: Array<{
      category: string;
      metric_name: string;
      value: number;
      unit?: string;
    }>;
  }) => api.post('/api/v1/entries', data),
  update: (id: number, data: {
    title?: string;
    content?: string;
    category_id?: number;
    priority?: string;
    status?: string;
    tags?: string[];
    created_at?: string;
    metrics?: Array<{
      category: string;
      metric_name: string;
      value: number;
      unit?: string;
    }>;
  }) => api.put(`/api/v1/entries/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/entries/${id}`),
};

// Metrics endpoints
export const metrics = {
  getAll: (entry_id?: number, category?: string) => {
    let url = '/api/v1/metrics';
    if (entry_id) url += `?entry_id=${entry_id}`;
    if (category) url += `${entry_id ? '&' : '?'}category=${category}`;
    return api.get(url);
  },
  getById: (id: number) => api.get(`/api/v1/metrics/${id}`),
  create: (data: {
    category: string;
    metric_name: string;
    value: number;
    unit?: string;
    entry_id: number;
  }) => api.post('/api/v1/metrics', data),
  update: (id: number, data: {
    category?: string;
    metric_name?: string;
    value?: number;
    unit?: string;
    entry_id?: number;
  }) => api.put(`/api/v1/metrics/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/metrics/${id}`),
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