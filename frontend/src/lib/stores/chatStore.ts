import { writable } from 'svelte/store';
import type { ChatResponse } from '../api/backend';

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: string[];
  isLoading?: boolean;
}

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}

// Initial state
const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
};

// Create writable store
export const chatStore = writable<ChatState>(initialState);

// Helper functions untuk update store
export const chatActions = {
  // Add user message
  addUserMessage: (content: string) => {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      type: 'user',
      content,
      timestamp: new Date(),
    };

    chatStore.update(state => ({
      ...state,
      messages: [...state.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    return userMessage.id;
  },

  // Add assistant message
  addAssistantMessage: (response: ChatResponse) => {
    const assistantMessage: ChatMessage = {
      id: crypto.randomUUID(),
      type: 'assistant',
      content: response.answer,
      timestamp: new Date(response.timestamp),
      sources: response.sources,
    };

    chatStore.update(state => ({
      ...state,
      messages: [...state.messages, assistantMessage],
      isLoading: false,
    }));
  },

  // Set loading state
  setLoading: (isLoading: boolean) => {
    chatStore.update(state => ({
      ...state,
      isLoading,
    }));
  },

  // Set error
  setError: (error: string | null) => {
    chatStore.update(state => ({
      ...state,
      error,
      isLoading: false,
    }));
  },

  // Clear chat
  clearChat: () => {
    chatStore.set(initialState);
  },

  // Add loading message placeholder
  addLoadingMessage: () => {
    const loadingMessage: ChatMessage = {
      id: crypto.randomUUID(),
      type: 'assistant',
      content: '',
      timestamp: new Date(),
      isLoading: true,
    };

    chatStore.update(state => ({
      ...state,
      messages: [...state.messages, loadingMessage],
    }));

    return loadingMessage.id;
  },

  // Update loading message with actual response
  updateLoadingMessage: (messageId: string, response: ChatResponse) => {
    chatStore.update(state => ({
      ...state,
      messages: state.messages.map(msg => 
        msg.id === messageId 
          ? {
              ...msg,
              content: response.answer,
              sources: response.sources,
              timestamp: new Date(response.timestamp),
              isLoading: false,
            }
          : msg
      ),
      isLoading: false,
    }));
  },
};
