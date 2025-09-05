# الفقيه AI - نظام ذكاء اصطناعي للفتاوى الشرعية

نظام ذكاء اصطناعي متقدم للفتاوى الشرعية مبني بـ Next.js و TypeScript، يوفر استشارات من المذاهب الأربعة والبحث في القرآن الكريم والسنة النبوية.

## 🕌 نظرة عامة

الفقيه AI هو نظام ذكاء اصطناعي متقدم للفتاوى الشرعية يوفر:

- **استشارات من المذاهب الأربعة** (الحنفي، المالكي، الشافعي، الحنبلي)
- **البحث في القرآن الكريم والسنة النبوية**
- **واجهة مستخدم حديثة ومتجاوبة**
- **نظام إدارة API keys متقدم**
- **معالجة أخطاء محسنة**

## 🚀 الميزات

### ✅ **Frontend (Next.js + TypeScript)**
- **App Router** - أحدث نظام توجيه في Next.js
- **TypeScript** - نوعية بيانات قوية
- **Tailwind CSS** - تصميم متجاوب وحديث
- **Lucide React** - أيقونات جميلة ومتسقة
- **RTL Support** - دعم كامل للغة العربية

### ✅ **Backend (API Routes)**
- **Next.js API Routes** - API endpoints مدمجة
- **Google Gemini AI** - ذكاء اصطناعي متقدم
- **Type Safety** - أنواع بيانات محكمة
- **Error Handling** - معالجة أخطاء شاملة

### ✅ **Services**
- **MadhhabService** - خدمة المذاهب الأربعة
- **QuranSunnahService** - خدمة القرآن والسنة
- **ApiKeyService** - إدارة API keys

## 📁 هيكل المشروع

```
al-faqih-ai-nextjs/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── api/               # API Routes
│   │   │   ├── chat/          # محادثة المذاهب
│   │   │   ├── quran-sunnah/  # القرآن والسنة
│   │   │   ├── test-api-key/  # اختبار API key
│   │   │   └── get-default-api-key/
│   │   ├── madhahib/          # صفحة المذاهب
│   │   ├── quran-sunnah/      # صفحة القرآن والسنة
│   │   ├── api-settings/      # إعدادات API
│   │   └── page.tsx           # الصفحة الرئيسية
│   ├── components/            # مكونات React
│   │   └── ApiKeyManager.tsx  # إدارة API keys
│   ├── services/              # الخدمات
│   │   ├── madhhabService.ts  # خدمة المذاهب
│   │   ├── quranSunnahService.ts
│   │   └── apiKeyService.ts   # خدمة API keys
│   ├── types/                 # أنواع البيانات
│   │   └── index.ts
│   └── config/                # الإعدادات
│       └── index.ts
├── public/                    # الملفات الثابتة
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

## 🛠️ التثبيت والتشغيل

### 1. **تثبيت المتطلبات**
```bash
npm install
```

### 2. **إعداد مفاتيح API**
النظام يعمل بدون ملف `.env` - مفاتيح API محفوظة في IndexedDB في المتصفح:
1. اذهب إلى [Google AI Studio](https://aistudio.google.com/apikey)
2. سجل الدخول بحساب Google
3. انقر على "Create API Key"
4. انسخ المفتاح وأدخله في واجهة التطبيق

### 3. **تشغيل التطبيق**
```bash
# وضع التطوير
npm run dev

# بناء الإنتاج
npm run build
npm start
```

### 4. **فتح المتصفح**
```
http://localhost:3000
```

## 🔧 التطوير

### **الأوامر المتاحة**
```bash
npm run dev          # تشغيل في وضع التطوير
npm run build        # بناء المشروع
npm run start        # تشغيل الإنتاج
npm run lint         # فحص الكود
```

### **إضافة مكون جديد**
```typescript
// src/components/NewComponent.tsx
'use client';

interface NewComponentProps {
  title: string;
}

export default function NewComponent({ title }: NewComponentProps) {
  return (
    <div className="p-4">
      <h2>{title}</h2>
    </div>
  );
}
```

### **إضافة API route جديد**
```typescript
// src/app/api/new-endpoint/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  return NextResponse.json({ message: 'Hello World' });
}
```

## 🎨 التخصيص

### **الألوان (Tailwind)**
```css
/* يمكن تخصيص الألوان في tailwind.config.js */
colors: {
  primary: '#2c3e50',
  secondary: '#3498db',
  success: '#28a745',
  warning: '#ffc107',
  danger: '#dc3545',
}
```

### **المذاهب**
```typescript
// src/config/index.ts
madhahib: {
  hanafi: {
    name: 'الحنفي',
    founder: 'الإمام أبو حنيفة النعمان بن ثابت',
    // ... المزيد من الإعدادات
  }
}
```

## 🚀 النشر

### **Vercel (مستحسن)**
```bash
# تثبيت Vercel CLI
npm i -g vercel

# النشر
vercel --prod
```

### **Netlify**
```bash
# بناء المشروع
npm run build

# رفع مجلد .next
```

### **Docker**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔒 الأمان

- **API Keys** - تخزين آمن في IndexedDB
- **Type Safety** - فحص الأنواع في وقت التطوير
- **Input Validation** - التحقق من المدخلات
- **Error Boundaries** - معالجة الأخطاء

## 📊 الأداء

- **Next.js 15** - أحدث إصدار مع تحسينات الأداء
- **App Router** - تحميل أسرع للصفحات
- **TypeScript** - كود أكثر كفاءة
- **Tailwind CSS** - ملفات CSS محسنة

## 🤝 المساهمة

1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 📞 الدعم

- **GitHub Issues** - للإبلاغ عن المشاكل
- **Documentation** - للأسئلة التقنية
- **Community** - للمناقشات العامة

---

**الفقيه AI** - نظام ذكاء اصطناعي للفتاوى الشرعية 🕌

مبني بـ ❤️ باستخدام Next.js و TypeScript
