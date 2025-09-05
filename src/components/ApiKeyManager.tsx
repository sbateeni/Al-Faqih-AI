'use client';

import { useState } from 'react';
import { Eye, EyeOff, Save, TestTube, ExternalLink, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { ApiKeyState } from '@/types';

interface ApiKeyManagerProps {
  apiKeyState: ApiKeyState;
  onApiKeyChange: (state: ApiKeyState) => void;
}

export default function ApiKeyManager({ apiKeyState, onApiKeyChange }: ApiKeyManagerProps) {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);

  const showMessage = (type: 'success' | 'error' | 'info', text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 5000);
  };

  const handleSave = async () => {
    if (!apiKey.trim()) {
      showMessage('error', 'يرجى إدخال مفتاح API أولاً');
      return;
    }

    setLoading(true);
    try {
      // التحقق من صحة المفتاح أولاً
      const response = await fetch('/api/test-api-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apiKey }),
      });

      const data = await response.json();
      
      if (response.ok && data.status === 'success') {
        // حفظ المفتاح في IndexedDB
        const apiKeyService = new (await import('@/services/apiKeyService')).ApiKeyService();
        const saved = await apiKeyService.saveApiKey(apiKey, 'user');
        
        if (saved) {
          showMessage('success', 'تم حفظ مفتاح API بنجاح!');
          onApiKeyChange({
            key: apiKey,
            isValid: true,
            isDefault: false,
            lastUsed: new Date().toISOString(),
          });
        } else {
          showMessage('error', 'حدث خطأ أثناء حفظ المفتاح');
        }
      } else {
        showMessage('error', data.message || 'مفتاح API غير صالح');
      }
    } catch (error) {
      showMessage('error', 'حدث خطأ أثناء حفظ المفتاح');
    } finally {
      setLoading(false);
    }
  };

  const handleTest = async () => {
    const keyToTest = apiKey || apiKeyState.key;
    if (!keyToTest) {
      showMessage('error', 'يرجى إدخال مفتاح API أولاً');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/test-api-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apiKey: keyToTest }),
      });

      const data = await response.json();
      
      if (response.ok && data.status === 'success') {
        showMessage('success', '✅ تم التحقق من المفتاح بنجاح!');
        onApiKeyChange({
          key: keyToTest,
          isValid: true,
          isDefault: false,
          lastUsed: new Date().toISOString(),
        });
      } else {
        showMessage('error', data.message || 'فشل التحقق من المفتاح');
      }
    } catch (error) {
      showMessage('error', 'حدث خطأ في الاتصال بالخادم');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = () => {
    if (apiKeyState.isValid) {
      return <CheckCircle className="w-5 h-5 text-green-500" />;
    } else if (apiKeyState.key) {
      return <XCircle className="w-5 h-5 text-red-500" />;
    } else {
      return <AlertCircle className="w-5 h-5 text-yellow-500" />;
    }
  };

  const getStatusText = () => {
    if (apiKeyState.isValid) {
      return 'مفتاح API صالح ويعمل بشكل صحيح';
    } else if (apiKeyState.key) {
      return 'مفتاح API غير صالح أو لا يعمل';
    } else {
      return 'لا يوجد مفتاح API محفوظ';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        إعدادات مفتاح API
      </h2>

      {/* حالة المفتاح الحالي */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-3 mb-2">
          {getStatusIcon()}
          <span className="font-medium text-gray-700">{getStatusText()}</span>
        </div>
        {apiKeyState.key && (
          <p className="text-sm text-gray-600 font-mono">
            {apiKeyState.key.substring(0, 10)}...
          </p>
        )}
      </div>

      {/* حقل إدخال المفتاح */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          مفتاح Gemini API
        </label>
        <div className="relative">
          <input
            type={showKey ? 'text' : 'password'}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="مثال: AIzaSy..."
            className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="button"
            onClick={() => setShowKey(!showKey)}
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
          >
            {showKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
        <p className="mt-2 text-sm text-gray-600">
          <a
            href="https://aistudio.google.com/apikey"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
          >
            <ExternalLink className="w-4 h-4" />
            الحصول على مفتاح API من Google AI Studio
          </a>
        </p>
      </div>

      {/* أزرار التحكم */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={handleSave}
          disabled={loading || !apiKey.trim()}
          className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Save className="w-5 h-5" />
          {loading ? 'جاري الحفظ...' : 'حفظ المفتاح'}
        </button>
        <button
          onClick={handleTest}
          disabled={loading || (!apiKey.trim() && !apiKeyState.key)}
          className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <TestTube className="w-5 h-5" />
          {loading ? 'جاري الاختبار...' : 'فحص الاتصال'}
        </button>
      </div>

      {/* رسائل الحالة */}
      {message && (
        <div className={`p-4 rounded-lg flex items-center gap-2 ${
          message.type === 'success' ? 'bg-green-100 text-green-800' :
          message.type === 'error' ? 'bg-red-100 text-red-800' :
          'bg-blue-100 text-blue-800'
        }`}>
          {message.type === 'success' && <CheckCircle className="w-5 h-5" />}
          {message.type === 'error' && <XCircle className="w-5 h-5" />}
          {message.type === 'info' && <AlertCircle className="w-5 h-5" />}
          <span>{message.text}</span>
        </div>
      )}
    </div>
  );
}
