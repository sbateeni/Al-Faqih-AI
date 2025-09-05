'use client';

import { ArrowRight, Star, Users, Shield, Zap, Building2, BookOpen, Settings } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50" dir="rtl">
      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white overflow-hidden relative">
        {/* Background decorations */}
        <div className="absolute inset-0 bg-black bg-opacity-10"></div>
        <div className="absolute top-10 left-10 w-72 h-72 bg-white bg-opacity-5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-white bg-opacity-5 rounded-full blur-3xl"></div>
        
        <div className="container mx-auto px-4 text-center relative z-10">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-7xl font-bold mb-8 leading-tight">
              مرحباً بك في الفقيه AI
            </h1>
            <p className="text-xl md:text-2xl mb-12 text-blue-100 leading-relaxed max-w-3xl mx-auto">
              نظام ذكاء اصطناعي متطور للفتاوى الشرعية يوفر الإرشاد الديني وفقاً للمذاهب الأربعة مع أدوات بحث في القرآن والسنة
            </p>
            <div className="flex flex-wrap justify-center gap-6">
              <Link 
                href="/madhahib"
                className="group bg-white text-blue-600 px-8 py-4 rounded-xl font-bold hover:bg-blue-50 transition-all duration-300 transform hover:scale-105 flex items-center gap-3 shadow-lg"
              >
                <Building2 className="w-6 h-6" />
                المذاهب الأربعة
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link 
                href="/quran-sunnah"
                className="group bg-transparent border-2 border-white text-white px-8 py-4 rounded-xl font-bold hover:bg-white hover:text-blue-600 transition-all duration-300 transform hover:scale-105 flex items-center gap-3 shadow-lg"
              >
                <BookOpen className="w-6 h-6" />
                القرآن والسنة
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-16">
        {/* Features Grid */}
        <div className="max-w-6xl mx-auto mb-20">
          <h2 className="text-4xl font-bold text-center text-gray-800 mb-4">اكتشف خدماتنا</h2>
          <p className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto">
            اختر من بين خدماتنا المتنوعة للحصول على الإرشاد الديني والبحث الشرعي
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* المذاهب الأربعة */}
            <Link 
              href="/madhahib"
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-3 p-8 text-center border border-gray-100 hover:border-blue-200"
            >
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                <Building2 className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">المذاهب الأربعة</h3>
              <p className="text-gray-600 leading-relaxed mb-6 min-h-[4rem]">
                استشر المذاهب الأربعة في المسائل الفقهية واحصل على الفتاوى من مصادرها الأصلية
              </p>
              <div className="flex items-center justify-center text-blue-600 font-medium group-hover:text-blue-700">
                ابدأ الآن
                <ArrowRight className="w-4 h-4 mr-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            {/* القرآن والسنة */}
            <Link 
              href="/quran-sunnah"
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-3 p-8 text-center border border-gray-100 hover:border-green-200"
            >
              <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                <BookOpen className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">القرآن والسنة</h3>
              <p className="text-gray-600 leading-relaxed mb-6 min-h-[4rem]">
                ابحث في القرآن الكريم والسنة النبوية واحصل على الأدلة والتفاسير
              </p>
              <div className="flex items-center justify-center text-green-600 font-medium group-hover:text-green-700">
                ابدأ الآن
                <ArrowRight className="w-4 h-4 mr-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            {/* إعدادات API */}
            <Link 
              href="/api-settings"
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-3 p-8 text-center border border-gray-100 hover:border-purple-200"
            >
              <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                <Settings className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">إعدادات API</h3>
              <p className="text-gray-600 leading-relaxed mb-6 min-h-[4rem]">
                إدارة مفاتيح API والتحقق من صحة الاتصال مع خدمات الذكاء الاصطناعي
              </p>
              <div className="flex items-center justify-center text-purple-600 font-medium group-hover:text-purple-700">
                إدارة الإعدادات
                <ArrowRight className="w-4 h-4 mr-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <section className="max-w-6xl mx-auto mb-20">
          <div className="bg-white rounded-2xl shadow-xl p-12 border border-gray-100">
            <h3 className="text-4xl font-bold text-center text-gray-800 mb-4">مميزات النظام</h3>
            <p className="text-lg text-center text-gray-600 mb-12 max-w-2xl mx-auto">
              نظام متطور يجمع بين التقنية الحديثة والمعرفة الشرعية الأصيلة
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Star className="w-8 h-8 text-white" />
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-3">دقة عالية</h4>
                <p className="text-gray-600 leading-relaxed">إجابات دقيقة ومستندة إلى المصادر الشرعية المعتمدة</p>
              </div>
              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Users className="w-8 h-8 text-white" />
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-3">شامل</h4>
                <p className="text-gray-600 leading-relaxed">يغطي جميع المذاهب الأربعة والقرآن والسنة</p>
              </div>
              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Shield className="w-8 h-8 text-white" />
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-3">آمن</h4>
                <p className="text-gray-600 leading-relaxed">حماية كاملة لبياناتك ومفاتيح API</p>
              </div>
              <div className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Zap className="w-8 h-8 text-white" />
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-3">سريع</h4>
                <p className="text-gray-600 leading-relaxed">استجابة فورية لجميع استفساراتك</p>
              </div>
            </div>
          </div>
        </section>

        {/* How to Use */}
        <section className="max-w-6xl mx-auto">
          <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-12 border border-gray-100">
            <h3 className="text-4xl font-bold text-center text-gray-800 mb-4">كيفية الاستخدام</h3>
            <p className="text-lg text-center text-gray-600 mb-12 max-w-2xl mx-auto">
              خطوات بسيطة للبدء في استخدام النظام والحصول على الإرشاد الشرعي
            </p>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl font-bold group-hover:scale-110 transition-transform duration-300">
                  1
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-4">أدخل مفتاح API</h4>
                <p className="text-gray-600 leading-relaxed">احصل على مفتاح API من Google AI Studio وأدخله في صفحة الإعدادات</p>
              </div>
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 text-white rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl font-bold group-hover:scale-110 transition-transform duration-300">
                  2
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-4">اختر نوع الاستشارة</h4>
                <p className="text-gray-600 leading-relaxed">اختر بين المذاهب الأربعة أو البحث في القرآن والسنة</p>
              </div>
              <div className="text-center group">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl font-bold group-hover:scale-110 transition-transform duration-300">
                  3
                </div>
                <h4 className="text-xl font-bold text-gray-800 mb-4">احصل على الإجابة</h4>
                <p className="text-gray-600 leading-relaxed">احصل على إجابة شاملة ومفصلة لسؤالك</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-800 text-white py-12 mt-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <Building2 className="w-7 h-7 text-white" />
              </div>
              <h4 className="text-2xl font-bold">الفقيه AI</h4>
            </div>
            <p className="text-gray-300 mb-8 text-lg leading-relaxed max-w-2xl mx-auto">
              نظام ذكاء اصطناعي للفتاوى الشرعية - مبني بـ❤️ باستخدام Next.js و TypeScript
            </p>
            <div className="flex justify-center gap-8 text-sm text-gray-400">
              <span>© 2024 الفقيه AI</span>
              <span>•</span>
              <span>جميع الحقوق محفوظة</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}