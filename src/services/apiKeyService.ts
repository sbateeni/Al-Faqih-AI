import { ApiKeyData, ApiKeyState } from '@/types';
import { config } from '@/config';

export class ApiKeyService {
  private dbName: string;
  private dbVersion: number;
  private storeName: string;

  constructor() {
    this.dbName = config.database.name;
    this.dbVersion = config.database.version;
    this.storeName = config.database.storeName;
  }

  // فتح قاعدة البيانات
  private async openDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' });
        }
      };
    });
  }

  // حفظ مفتاح API
  async saveApiKey(apiKey: string, keyType: string = 'user'): Promise<boolean> {
    try {
      const db = await this.openDB();
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      
      const apiKeyData: ApiKeyData = {
        id: 'current_api_key',
        apiKey,
        keyType,
        isDefault: false,
        createdAt: new Date().toISOString(),
        lastUsed: new Date().toISOString(),
      };

      await new Promise<void>((resolve, reject) => {
        const request = store.put(apiKeyData);
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });

      return true;
    } catch (error) {
      console.error('Error saving API key:', error);
      return false;
    }
  }

  // جلب مفتاح API المحفوظ
  async getApiKey(): Promise<ApiKeyData | null> {
    try {
      const db = await this.openDB();
      const transaction = db.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      
      return new Promise((resolve, reject) => {
        const request = store.get('current_api_key');
        request.onsuccess = () => resolve(request.result || null);
        request.onerror = () => reject(request.error);
      });
    } catch (error) {
      console.error('Error getting API key:', error);
      return null;
    }
  }

  // حذف مفتاح API
  async deleteApiKey(): Promise<boolean> {
    try {
      const db = await this.openDB();
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      
      await new Promise<void>((resolve, reject) => {
        const request = store.delete('current_api_key');
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });

      return true;
    } catch (error) {
      console.error('Error deleting API key:', error);
      return false;
    }
  }

  // تحديث آخر استخدام
  async updateLastUsed(): Promise<boolean> {
    try {
      const apiKeyData = await this.getApiKey();
      if (!apiKeyData) return false;

      const db = await this.openDB();
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      
      const updatedData = {
        ...apiKeyData,
        lastUsed: new Date().toISOString(),
      };

      await new Promise<void>((resolve, reject) => {
        const request = store.put(updatedData);
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });

      return true;
    } catch (error) {
      console.error('Error updating last used:', error);
      return false;
    }
  }

  // جلب حالة API key
  async getApiKeyState(): Promise<ApiKeyState> {
    try {
      const apiKeyData = await this.getApiKey();
      
      if (!apiKeyData) {
        return {
          key: null,
          isValid: false,
          isDefault: true,
          lastUsed: null,
        };
      }

      return {
        key: apiKeyData.apiKey,
        isValid: true, // سيتم التحقق من الصحة في مكان آخر
        isDefault: apiKeyData.isDefault,
        lastUsed: apiKeyData.lastUsed,
      };
    } catch (error) {
      console.error('Error getting API key state:', error);
      return {
        key: null,
        isValid: false,
        isDefault: true,
        lastUsed: null,
      };
    }
  }

  // التحقق من صحة مفتاح API
  async validateApiKey(apiKey: string): Promise<boolean> {
    try {
      const response = await fetch('/api/test-api-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apiKey }),
      });

      const data = await response.json();
      return response.ok && data.status === 'success';
    } catch (error) {
      console.error('Error validating API key:', error);
      return false;
    }
  }

  // جلب المفتاح الافتراضي
  async getDefaultApiKey(): Promise<string | null> {
    try {
      const response = await fetch('/api/get-default-api-key');
      const data = await response.json();
      
      if (response.ok && data.status === 'success') {
        return data.apiKey;
      }
      
      return null;
    } catch (error) {
      console.error('Error getting default API key:', error);
      return null;
    }
  }

  // حفظ المفتاح الافتراضي في IndexedDB
  async saveDefaultApiKey(): Promise<boolean> {
    try {
      const defaultKey = await this.getDefaultApiKey();
      if (!defaultKey) return false;

      const db = await this.openDB();
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      
      const apiKeyData: ApiKeyData = {
        id: 'default_api_key',
        apiKey: defaultKey,
        keyType: 'default',
        isDefault: true,
        createdAt: new Date().toISOString(),
        lastUsed: new Date().toISOString(),
      };

      await new Promise<void>((resolve, reject) => {
        const request = store.put(apiKeyData);
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });

      return true;
    } catch (error) {
      console.error('Error saving default API key:', error);
      return false;
    }
  }

  // جلب جميع مفاتيح API المحفوظة
  async getAllApiKeys(): Promise<ApiKeyData[]> {
    try {
      const db = await this.openDB();
      const transaction = db.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      
      return new Promise((resolve, reject) => {
        const request = store.getAll();
        request.onsuccess = () => resolve(request.result || []);
        request.onerror = () => reject(request.error);
      });
    } catch (error) {
      console.error('Error getting all API keys:', error);
      return [];
    }
  }

  // جلب أفضل مفتاح API متاح
  async getBestAvailableApiKey(): Promise<string | null> {
    try {
      // أولاً جرب المفتاح المحفوظ
      const savedKey = await this.getApiKey();
      if (savedKey && savedKey.isValid) {
        return savedKey.apiKey;
      }

      // ثم جرب المفتاح الافتراضي
      const defaultKey = await this.getDefaultApiKey();
      if (defaultKey) {
        return defaultKey;
      }

      return null;
    } catch (error) {
      console.error('Error getting best available API key:', error);
      return null;
    }
  }
}
