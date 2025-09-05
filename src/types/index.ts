// Types for Al-Faqih AI
// أنواع البيانات لنظام الفقيه AI

export interface ApiResponse<T = any> {
  status: 'success' | 'error';
  message?: string;
  data?: T;
}

export interface MadhhabInfo {
  name: string;
  founder: string;
  period: string;
  sources: string[];
  methodology: string;
  influence: string[];
  scholars: string[];
}

export interface MadhhabResponse {
  madhhab: string;
  answer: string;
  timestamp: string;
}

export interface QuranSunnahResponse {
  quran?: {
    full_response: string;
    sections: Record<string, string>;
  };
  hadith?: {
    full_response: string;
    sections: Record<string, string>;
  };
  quran_error?: string;
  hadith_error?: string;
}

export interface ApiKeyData {
  id: string;
  apiKey: string;
  keyType: string;
  isDefault: boolean;
  createdAt: string;
  lastUsed: string;
}

export interface ChatRequest {
  question: string;
  madhhab?: string;
}

export interface QuranSunnahRequest {
  question: string;
  type: 'quran' | 'hadith' | 'both';
}

export interface TestApiKeyRequest {
  apiKey: string;
}

export type MadhhabType = 'hanafi' | 'maliki' | 'shafii' | 'hanbali' | 'all';

export interface UIState {
  loading: boolean;
  error: string | null;
  success: string | null;
}

export interface ApiKeyState {
  key: string | null;
  isValid: boolean;
  isDefault: boolean;
  lastUsed: string | null;
}
