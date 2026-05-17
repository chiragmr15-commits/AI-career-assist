import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem('access_token', response.data.access);
          api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch (err) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

export const authService = {
  register: (data) => api.post('/auth/register/', data),
  login: (username, password) => api.post('/auth/login/', { username, password }),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.put('/auth/profile/', data),
};

export const resumeService = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume/upload/', formData);
  },
  analyze: () => api.post('/resume/analyze/'),
  getDetail: () => api.get('/resume/detail/'),
  updateDetail: (data) => api.put('/resume/detail/', data),
  addSkill: (data) => api.post('/resume/add-skill/', data),
  jobMatch: (jobDescription) => api.post('/resume/job-match/', { job_description: jobDescription }),
};

export const careerService = {
  getRecommendation: (interests) => api.post('/career/recommendation/', { interests }),
  getPaths: (career) => api.get('/career/paths/', { params: { career } }),
  getProfile: () => api.get('/career/profile/'),
  updateProfile: (data) => api.put('/career/profile/', data),
  getSkillGap: () => api.get('/career/skill-gap/'),
};

export const interviewService = {
  generateInterview: (data) => api.post('/interview/generate/', data),
  getSession: (sessionId) => api.get(`/interview/session/${sessionId}/`),
  submitAnswer: (questionId, answer) => api.post(`/interview/answer/${questionId}/`, { answer }),
  completeInterview: (sessionId) => api.post(`/interview/complete/${sessionId}/`),
  getHistory: () => api.get('/interview/history/'),
  getTemplates: () => api.get('/interview/templates/'),
};

export const emotionService = {
  addEntry: (data) => api.post('/emotion/add/', data),
  getHistory: (days) => api.get('/emotion/history/', { params: { days } }),
  getTrend: () => api.get('/emotion/trend/'),
  getTips: () => api.get('/emotion/tips/'),
  getStats: () => api.get('/emotion/stats/'),
};

export default api;
