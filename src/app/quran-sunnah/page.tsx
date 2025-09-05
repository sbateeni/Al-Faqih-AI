'use client';

import { useState, useEffect } from 'react';
import { Send, Loader2, CheckCircle, XCircle, BookOpen, Scroll } from 'lucide-react';
import { QuranSunnahResponse, ApiKeyState } from '@/types';

export default function QuranSunnahPage() {
  const [question, setQuestion] = useState('');
  const [searchType, setSearchType] = useState<'quran' | 'hadith' | 'both'>('both');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QuranSunnahResponse | null>(null);
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
      const response = await fetch('/api/quran-sunnah', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(apiKeyState.key && { 'GEMINI_API_KEY': apiKeyState.key }),
        },
        body: JSON.stringify({
          question: question.trim(),
          type: searchType,
        }),
      });

      const data = await response.json();

      if (response.ok && data.status === 'success') {
        setResponse(data.data);
      } else {
        setError(data.message || 'حدث خطأ أثناء معالجة طلبك');
      }
    } catch (error) {
      setError('حدث خطأ في الاتصال بالخادم');
    } finally {
      setLoading(false);
    }
  };

  const renderSection = (title: string, content: string) => (
    <div className="mb-6">
      <h4 className="text-lg font-bold text-gray-800 mb-3 border-b border-gray-200 pb-2">
        {title}
      </h4>
      <div className="prose prose-lg max-w-none">
        <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
          {content}
        </pre>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-green-50" dir="rtl">
      <div className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">القرآن والسنة</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            ابحث في القرآن الكريم والسنة النبوية واحصل على الأدلة والتفاسير
          </p>
        </div>

        {/* Question Form */}
        <div className="max-w-4xl mx-auto mb-8">
          <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">البحث في القرآن والسنة</h2>
            
            {/* API Status */}
            <div className="bg-gray-50 rounded-xl p-4 mb-6">
              <div className="flex items-center gap-3">
                {apiKeyState.isValid ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : (
                  <XCircle className="w-5 h-5 text-orange-500" />
                )}
                <span className="font-medium text-gray-700">
                  {apiKeyState.isValid ? 'مفتاح API صالح' : 'سيتم استخدام المفتاح الافتراضي'}
                </span>
              </div>
            </div>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                نوع البحث
              </label>
              <div className="grid grid-cols-3 gap-4">
                <button
                  type="button"
                  onClick={() => setSearchType('quran')}
                  className={`p-4 rounded-lg border-2 flex items-center justify-center gap-2 transition-colors ${
                    searchType === 'quran'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <BookOpen className="w-5 h-5" />
                  القرآن فقط
                </button>
                <button
                  type="button"
                  onClick={() => setSearchType('hadith')}
                  className={`p-4 rounded-lg border-2 flex items-center justify-center gap-2 transition-colors ${
                    searchType === 'hadith'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Scroll className="w-5 h-5" />
                  السنة فقط
                </button>
                <button
                  type="button"
                  onClick={() => setSearchType('both')}
                  className={`p-4 rounded-lg border-2 flex items-center justify-center gap-2 transition-colors ${
                    searchType === 'both'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <BookOpen className="w-5 h-5" />
                  <Scroll className="w-5 h-5" />
                  كلاهما
                </button>
              </div>
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
              className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-4 px-6 rounded-xl hover:from-green-700 hover:to-green-800 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium text-lg shadow-lg transition-all duration-300"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  جاري البحث...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  البحث
                </>
              )}
            </button>
          </form>
        </div>

        {/* Response */}
        {response && (
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h3 className="text-xl font-bold text-gray-800 mb-6">نتائج البحث</h3>
              
              {/* Quran Response */}
              {response.quran && (
                <div className="mb-8">
                  <div className="flex items-center gap-2 mb-4">
                    <BookOpen className="w-6 h-6 text-green-600" />
                    <h4 className="text-lg font-bold text-gray-800">القرآن الكريم</h4>
                  </div>
                  
                  {response.quran.sections && Object.keys(response.quran.sections).length > 0 ? (
                    Object.entries(response.quran.sections).map(([sectionTitle, sectionContent]) =>
                      renderSection(sectionTitle, sectionContent)
                    )
                  ) : (
                    <div className="prose prose-lg max-w-none">
                      <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
                        {response.quran.full_response}
                      </pre>
                    </div>
                  )}
                </div>
              )}

              {/* Hadith Response */}
              {response.hadith && (
                <div className="mb-8">
                  <div className="flex items-center gap-2 mb-4">
                    <Scroll className="w-6 h-6 text-blue-600" />
                    <h4 className="text-lg font-bold text-gray-800">السنة النبوية</h4>
                  </div>
                  
                  {response.hadith.sections && Object.keys(response.hadith.sections).length > 0 ? (
                    Object.entries(response.hadith.sections).map(([sectionTitle, sectionContent]) =>
                      renderSection(sectionTitle, sectionContent)
                    )
                  ) : (
                    <div className="prose prose-lg max-w-none">
                      <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
                        {response.hadith.full_response}
                      </pre>
                    </div>
                  )}
                </div>
              )}

              {/* Errors */}
              {response.quran_error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                  <div className="flex items-center gap-2">
                    <XCircle className="w-5 h-5 text-red-500" />
                    <span className="text-red-700 font-medium">خطأ في البحث في القرآن: {response.quran_error}</span>
                  </div>
                </div>
              )}

              {response.hadith_error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                  <div className="flex items-center gap-2">
                    <XCircle className="w-5 h-5 text-red-500" />
                    <span className="text-red-700 font-medium">خطأ في البحث في السنة: {response.hadith_error}</span>
                  </div>
                </div>
              )}
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
      </div>
    </div>
  );
}
