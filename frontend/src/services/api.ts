import axios, { AxiosInstance } from 'axios';
import { ChatMessage, ChatResponse, RiderData, RankingEntry } from '../types';

// API URLs - fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live';

// Export WebSocket URL
export const getWebSocketUrl = () => WS_BASE_URL;

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatApi = {
  sendMessage: async (message: string, history: ChatMessage[] = []): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat/', {
      message,
      conversation_history: history,
    });
    return response.data;
  },

  quickQuery: async (query: string) => {
    const response = await api.post('/chat/quick', null, { params: { query } });
    return response.data;
  },
};

// Riders API
export const ridersApi = {
  getProfile: async (slug: string): Promise<RiderData> => {
    const response = await api.get<RiderData>(`/riders/${slug}`);
    return response.data;
  },

  getVictories: async (slug: string, year?: number) => {
    const response = await api.get(`/riders/${slug}/victories`, {
      params: year ? { year } : {},
    });
    return response.data;
  },

  getResults: async (slug: string, year?: number) => {
    const response = await api.get(`/riders/${slug}/results`, {
      params: year ? { year } : {},
    });
    return response.data;
  },

  search: async (query: string) => {
    const response = await api.get('/riders/search/', { params: { q: query } });
    return response.data;
  },
};

// Rankings API
export const rankingsApi = {
  getIndividual: async (limit = 50): Promise<{ ranking: RankingEntry[] }> => {
    const response = await api.get<{ ranking: RankingEntry[] }>('/rankings/individual', {
      params: { limit },
    });
    return response.data;
  },

  getTeams: async (limit = 20) => {
    const response = await api.get('/rankings/teams', { params: { limit } });
    return response.data;
  },

  getNations: async (limit = 30) => {
    const response = await api.get('/rankings/nations', { params: { limit } });
    return response.data;
  },
};

// Races API
export const racesApi = {
  getResults: async (raceSlug: string, year: number, stage?: number) => {
    const params: Record<string, unknown> = { year };
    if (stage) params.stage = stage;

    const response = await api.get(`/races/${raceSlug}`, { params });
    return response.data;
  },

  getStartlist: async (raceSlug: string, year: number) => {
    const response = await api.get(`/races/${raceSlug}/startlist`, {
      params: { year },
    });
    return response.data;
  },
};

// Teams API
export const teamsApi = {
  getInfo: async (teamSlug: string, year = 2024) => {
    const response = await api.get(`/teams/${teamSlug}`, { params: { year } });
    return response.data;
  },
};

// Stats API
export const statsApi = {
  getSummary: async () => {
    const response = await api.get('/stats/summary');
    return response.data;
  },
};

export default api;
