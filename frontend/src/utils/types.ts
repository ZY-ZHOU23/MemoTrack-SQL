export interface User {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Entry {
  id: number;
  title: string;
  content: string;
  category: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface AnalyticsData {
  entriesByCategory: Array<{
    category: string;
    count: number;
  }>;
  entriesByDate: Array<{
    date: string;
    count: number;
  }>;
  entriesByTag: Array<{
    tag: string;
    count: number;
  }>;
  totalEntries: number;
  totalCategories: number;
  totalTags: number;
  averageEntriesPerDay: number;
  mostActiveDay: string;
  mostUsedCategory: string;
  mostUsedTag: string;
}

export interface DashboardStats {
  totalEntries: number;
  totalCategories: number;
  totalTags: number;
  recentEntries: Array<{
    id: number;
    title: string;
    created_at: string;
  }>;
  entriesByCategory: Array<{
    category: string;
    count: number;
  }>;
  entriesByDate: Array<{
    date: string;
    count: number;
  }>;
}

export type TimeRange = '7d' | '30d' | '90d' | 'all'; 