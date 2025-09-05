'use client';

import { useState, useEffect } from 'react';
import { Send, Loader2, CheckCircle, XCircle } from 'lucide-react';
import Link from 'next/link';
import { config } from '@/config';
import { MadhhabType, ApiKeyState } from '@/types';

export default function MadhahibPage() {
  const [question, setQuestion] = useState('');
  const [selectedMadhhab, setSelectedMadhhab] = useState<MadhhabType>('all');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiKeyState, setApiKeyState] = useState<ApiKeyState>({
    key: null,
    isValid: false,
    isDefault: true,
    lastUsed: null,
  });

  useEffect(() => {
    // تحميل حالة API key
    loadApiKeyState();
  }, []);

  const loadApiKeyState = async () => {
    try {
      // تحميل حالة API key من IndexedDB
      const { ApiKeyService } = await import('@/services/apiKeyService');
      const apiKeyService = new ApiKeyService();
      const apiKeyState = await apiKeyService.getApiKeyState();
      setApiKeyState(apiKeyState);
    } catch (error) {
      console.error('خطأ في تحميل حالة API key:', error);
      setApiKeyState({
        key: null,
        isValid: false,
        isDefault: true,
        lastUsed: null,
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(apiKeyState.key && { 'GEMINI_API_KEY': apiKeyState.key }),
        },
        body: JSON.stringify({
          question: question.trim(),
          madhhab: selectedMadhhab,
        }),
      });

      const data = await response.json();

      if (response.ok && data.status === 'success') {
        setResponse(data.data.answer);
      } else {
        setError(data.message || 'حدث خطأ أثناء معالجة طلبك');
      }
    } catch (error) {
      setError('حدث خطأ في الاتصال بالخادم');
    } finally {
      setLoading(false);
    }
  };

  const madhhabOptions = [
    { value: 'all', label: 'جميع المذاهب الأربعة' },
    { value: 'hanafi', label: 'المذهب الحنفي' },
    { value: 'maliki', label: 'المذهب المالكي' },
    { value: 'shafii', label: 'المذهب الشافعي' },
    { value: 'hanbali', label: 'المذهب الحنبلي' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50" dir="rtl">
      <div className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">المذاهب الأربعة</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            استشر المذاهب الأربعة في المسائل الفقهية واحصل على الفتاوى من مصادرها الأصلية
          </p>
        </div>

        {/* Question Form */}
        <div className="max-w-4xl mx-auto mb-8">
          <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">اسأل المذاهب الأربعة</h2>
            
            {/* API Status */}
            <div className="bg-gray-50 rounded-xl p-4 mb-6">
              <div className="flex items-center gap-3">
                {apiKeyState.isValid ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : (
                  <XCircle className="w-5 h-5 text-orange-500" />
                )}
                <span className="font-medium text-gray-700">
                  {apiKeyState.isValid ? 'مفتاح API صالح' : 'يجب إدخال مفتاح API في صفحة الإعدادات'}
                </span>
                {!apiKeyState.isValid && (
                  <Link href="/api-settings" className="text-blue-600 hover:text-blue-700 underline mr-2">
                    الذهاب للإعدادات
                  </Link>
                )}
              </div>
            </div>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                اختر المذهب
              </label>
              <select
                value={selectedMadhhab}
                onChange={(e) => setSelectedMadhhab(e.target.value as MadhhabType)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {madhhabOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                السؤال
              </label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="اكتب سؤالك هنا..."
                rows={4}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-6 rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium text-lg shadow-lg transition-all duration-300"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  جاري المعالجة...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  إرسال السؤال
                </>
              )}
            </button>
          </form>
        </div>

        {/* Response */}
        {response && (
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h3 className="text-xl font-bold text-gray-800 mb-4">الإجابة</h3>
              <div className="prose prose-lg max-w-none">
                <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
                  {response}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center gap-2">
                <XCircle className="w-5 h-5 text-red-500" />
                <span className="text-red-700 font-medium">{error}</span>
              </div>
            </div>
          </div>
        )}

        {/* Madhahib Info */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-bold text-gray-800 mb-6">معلومات عن المذاهب الأربعة</h3>
            <div className="grid md:grid-cols-2 gap-6">
              {Object.entries(config.madhahib).map(([key, madhhab]) => (
                <div key={key} className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-bold text-lg text-gray-800 mb-2">{madhhab.name}</h4>
                  <p className="text-sm text-gray-600 mb-2">
                    <strong>المؤسس:</strong> {madhhab.founder}
                  </p>
                  <p className="text-sm text-gray-600 mb-2">
                    <strong>المنهجية:</strong> {madhhab.methodology}
                  </p>
                  <p className="text-sm text-gray-600">
                    <strong>الانتشار:</strong> {madhhab.influence.slice(0, 3).join('، ')}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
