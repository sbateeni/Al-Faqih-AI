'use client';

import { useState, useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react';
import ApiKeyManager from '@/components/ApiKeyManager';
import { ApiKeyState } from '@/types';

export default function ApiSettingsPage() {
  const [apiKeyState, setApiKeyState] = useState<ApiKeyState>({
    key: null,
    isValid: false,
    isDefault: false,
    lastUsed: null,
  });
  const [loading, setLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState<{
    api: 'checking' | 'working' | 'error';
  }>({
    api: 'checking',
  });

  useEffect(() => {
    loadApiKeyState();
    checkSystemStatus();
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

  const checkSystemStatus = async () => {
    setLoading(true);
    
    try {
      // فحص API الشخصي فقط
      if (apiKeyState.key) {
        const testResponse = await fetch('/api/test-api-key', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ apiKey: apiKeyState.key }),
        });
        
        const testData = await testResponse.json();
        setSystemStatus({
          api: testData.status === 'success' ? 'working' : 'error'
        });
      } else {
        setSystemStatus({
          api: 'error'
        });
      }
    } catch (error) {
      console.error('خطأ في فحص حالة النظام:', error);
      setSystemStatus({
        api: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: 'checking' | 'working' | 'error') => {
    switch (status) {
      case 'checking':
        return <RefreshCw className="w-5 h-5 text-yellow-500 animate-spin" />;
      case 'working':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
    }
  };

  const getStatusText = (status: 'checking' | 'working' | 'error') => {
    switch (status) {
      case 'checking':
        return 'جاري الفحص...';
      case 'working':
        return 'يعمل بشكل صحيح';
      case 'error':
        return 'لا يعمل';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-purple-50" dir="rtl">
      <div className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">إعدادات API</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            إدارة مفاتيح API والتحقق من صحة الاتصال مع خدمات الذكاء الاصطناعي
          </p>
        </div>

        {/* System Status */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">حالة مفتاح API</h2>
            
            <div className="max-w-2xl mx-auto">
              {/* User API Key Status */}
              <div className="p-6 border border-gray-200 rounded-lg">
                <div className="flex items-center gap-3 mb-3">
                  {getStatusIcon(systemStatus.api)}
                  <h3 className="text-lg font-bold text-gray-800">مفتاحك الشخصي</h3>
                </div>
                <p className="text-gray-600 mb-4">
                  {apiKeyState.key 
                    ? (systemStatus.api === 'working' 
                        ? 'مفتاحك الشخصي يعمل بشكل صحيح'
                        : systemStatus.api === 'error'
                        ? 'مفتاحك الشخصي لا يعمل'
                        : 'جاري فحص مفتاحك الشخصي...'
                      )
                    : 'يجب إدخال مفتاح API شخصي لاستخدام النظام'
                  }
                </p>
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  apiKeyState.key 
                    ? (systemStatus.api === 'working' 
                        ? 'bg-green-100 text-green-800'
                        : systemStatus.api === 'error'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                      )
                    : 'bg-orange-100 text-orange-800'
                }`}>
                  {apiKeyState.key ? getStatusText(systemStatus.api) : 'مطلوب'}
                </div>
              </div>
            </div>

            <div className="mt-8 flex justify-center">
              <button
                onClick={checkSystemStatus}
                disabled={loading}
                className="bg-gradient-to-r from-purple-600 to-purple-700 text-white px-8 py-3 rounded-xl hover:from-purple-700 hover:to-purple-800 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center gap-2 font-medium shadow-lg transition-all duration-300"
              >
                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
                {loading ? 'جاري الفحص...' : 'إعادة فحص النظام'}
              </button>
            </div>
          </div>
        </div>

        {/* API Key Manager */}
        <div className="max-w-2xl mx-auto mb-8">
          {/* Required API Key Notice */}
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 text-blue-600 mt-1" />
              <div>
                <h3 className="text-lg font-bold text-blue-800 mb-2">مفتاح API مطلوب</h3>
                <p className="text-blue-700 leading-relaxed">
                  لاستخدام النظام، يجب إدخال مفتاح API الخاص بك من Google AI Studio. لا يوجد مفتاح افتراضي متاح.
                </p>
              </div>
            </div>
          </div>
          
          <ApiKeyManager 
            apiKeyState={apiKeyState}
            onApiKeyChange={(newState) => {
              setApiKeyState(newState);
              // إعادة فحص النظام عند تغيير المفتاح
              setTimeout(() => {
                checkSystemStatus();
              }, 1000);
            }}
          />
        </div>

        {/* Information Section */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">معلومات مهمة</h2>
            
            <div className="space-y-6">
              <div className="p-6 bg-blue-50 rounded-lg">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-6 h-6 text-blue-600 mt-1" />
                  <div>
                    <h3 className="text-lg font-bold text-blue-800 mb-2">كيفية الحصول على مفتاح API</h3>
                    <ol className="list-decimal list-inside text-blue-700 space-y-2">
                      <li>اذهب إلى <a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener noreferrer" className="underline hover:text-blue-900">Google AI Studio</a></li>
                      <li>سجل الدخول بحساب Google الخاص بك</li>
                      <li>انقر على "Create API Key"</li>
                      <li>انسخ المفتاح وأدخله في النموذج أعلاه</li>
                    </ol>
                  </div>
                </div>
              </div>

              <div className="p-6 bg-green-50 rounded-lg">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-600 mt-1" />
                  <div>
                    <h3 className="text-lg font-bold text-green-800 mb-2">الأمان والخصوصية</h3>
                    <ul className="list-disc list-inside text-green-700 space-y-2">
                      <li>مفاتيح API محفوظة محلياً في متصفحك فقط</li>
                      <li>لا يتم إرسال مفاتيحك إلى خوادم خارجية</li>
                      <li>يمكنك حذف مفتاحك في أي وقت</li>
                      <li>تحكم كامل في مفاتيحك وبياناتك</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="p-6 bg-yellow-50 rounded-lg">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-6 h-6 text-yellow-600 mt-1" />
                  <div>
                    <h3 className="text-lg font-bold text-yellow-800 mb-2">ملاحظات مهمة</h3>
                    <ul className="list-disc list-inside text-yellow-700 space-y-2">
                      <li>تأكد من صحة مفتاح API قبل الاستخدام</li>
                      <li>مفتاح API مطلوب لتشغيل جميع وظائف النظام</li>
                      <li>احتفظ بنسخة احتياطية من مفتاحك في مكان آمن</li>
                      <li>يمكنك الحصول على مفتاح مجاني من Google AI Studio</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
