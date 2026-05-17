import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),

  setUser: (user) => set({ user }),
  setToken: (token) => {
    localStorage.setItem('access_token', token);
    set({ token, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, token: null, isAuthenticated: false });
  },
}));

export const useResumeStore = create((set) => ({
  resume: null,
  atsScore: 0,
  skills: [],
  analysis: null,

  setResume: (resume) => set({ resume }),
  setATSScore: (score) => set({ atsScore: score }),
  setSkills: (skills) => set({ skills }),
  setAnalysis: (analysis) => set({ analysis }),
}));

export const useCareerStore = create((set) => ({
  careerProfile: null,
  recommendations: null,
  skillGap: null,

  setCareerProfile: (profile) => set({ careerProfile: profile }),
  setRecommendations: (recommendations) => set({ recommendations }),
  setSkillGap: (gap) => set({ skillGap: gap }),
}));

export const useEmotionStore = create((set) => ({
  moodHistory: [],
  moodTrend: null,
  currentMood: null,

  setMoodHistory: (history) => set({ moodHistory: history }),
  setMoodTrend: (trend) => set({ moodTrend: trend }),
  setCurrentMood: (mood) => set({ currentMood: mood }),
}));
