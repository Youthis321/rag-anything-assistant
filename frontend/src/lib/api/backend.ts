// API client untuk backend RAG Anything Assistant
const API_BASE_URL = 'http://localhost:8000';

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  sources: string[];
  timestamp: string;
}

export interface StatsResponse {
  total_articles: number;
  total_projects: number;
  total_conversations: number;
  last_updated: string;
}

export interface HistoryResponse {
  date: string;
  conversations: Array<{
    id: string;
    question: string;
    answer: string;
    timestamp: string;
    sources: string[];
  }>;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  services: {
    rag_service: string;
    gemini_service: string;
    history_service: string;
  };
}

class BackendAPI {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Health check
  async health(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  // Chat dengan RAG
  async chat(question: string): Promise<ChatResponse> {
    return this.request<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify({ question }),
    });
  }

  // Get statistics
  async getStats(): Promise<StatsResponse> {
    return this.request<StatsResponse>('/stats');
  }

  // Get history by date
  async getHistory(date: string): Promise<HistoryResponse> {
    return this.request<HistoryResponse>(`/history/${date}`);
  }
}

export const backendAPI = new BackendAPI();
