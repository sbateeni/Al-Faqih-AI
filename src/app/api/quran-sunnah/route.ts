import { NextRequest, NextResponse } from 'next/server';
import { QuranSunnahService } from '@/services/quranSunnahService';
import { QuranSunnahRequest, ApiResponse } from '@/types';
import { config } from '@/config';

export async function POST(request: NextRequest) {
  try {
    const body: QuranSunnahRequest = await request.json();
    const { question, type = 'both' } = body;

    if (!question) {
      return NextResponse.json({
        status: 'error',
        message: 'الرجاء إدخال سؤال'
      }, { status: 400 });
    }

    // الحصول على API key من الـ headers - مطلوب من المستخدم
    const apiKey = request.headers.get('GEMINI_API_KEY');
    
    if (!apiKey) {
      return NextResponse.json({
        status: 'error',
        message: 'مفتاح API مطلوب. يرجى إدخال مفتاح API الخاص بك في صفحة الإعدادات.',
        requiresApiKey: true
      }, { status: 401 });
    }

    const quranSunnahService = new QuranSunnahService(apiKey);
    let result: ApiResponse<any>;

    switch (type) {
      case 'quran':
        result = await quranSunnahService.searchQuran(question);
        break;
      case 'hadith':
        result = await quranSunnahService.searchHadith(question);
        break;
      case 'both':
      default:
        result = await quranSunnahService.searchBoth(question);
        break;
    }

    if (result.status === 'error') {
      return NextResponse.json(result, { status: 500 });
    }

    return NextResponse.json({
      status: 'success',
      data: result.data
    });

  } catch (error) {
    console.error('Error in quran-sunnah API:', error);
    return NextResponse.json({
      status: 'error',
      message: 'حدث خطأ أثناء معالجة طلبك'
    }, { status: 500 });
  }
}
