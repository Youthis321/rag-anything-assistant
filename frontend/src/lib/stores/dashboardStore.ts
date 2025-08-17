import { writable } from 'svelte/store';
import type { StatsResponse } from '../api/backend';

export interface DashboardState {
  stats: StatsResponse | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

// Initial state
const initialState: DashboardState = {
  stats: null,
  isLoading: false,
  error: null,
  lastUpdated: null,
};

// Create writable store
export const dashboardStore = writable<DashboardState>(initialState);

// Helper functions untuk update store
export const dashboardActions = {
  // Set loading state
  setLoading: (isLoading: boolean) => {
    dashboardStore.update(state => ({
      ...state,
      isLoading,
      error: isLoading ? null : state.error,
    }));
  },

  // Set stats data
  setStats: (stats: StatsResponse) => {
    dashboardStore.update(state => ({
      ...state,
      stats,
      isLoading: false,
      error: null,
      lastUpdated: new Date(),
    }));
  },

  // Set error
  setError: (error: string) => {
    dashboardStore.update(state => ({
      ...state,
      error,
      isLoading: false,
    }));
  },

  // Clear error
  clearError: () => {
    dashboardStore.update(state => ({
      ...state,
      error: null,
    }));
  },

  // Reset store
  reset: () => {
    dashboardStore.set(initialState);
  },
};
