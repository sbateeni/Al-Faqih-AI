import { NextRequest, NextResponse } from 'next/server';
import { MadhhabService } from '@/services/madhhabService';
import { ChatRequest, ApiResponse } from '@/types';
import { config } from '@/config';

export async function POST(request: NextRequest) {
  try {
    const body: ChatRequest = await request.json();
    const { question, madhhab } = body;

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

    const madhhabService = new MadhhabService(apiKey);

    if (madhhab && madhhab !== 'all') {
      // إجابة من مذهب واحد محدد
      const madhhabMapping: Record<string, string> = {
        'hanafi': 'الحنفي',
        'maliki': 'المالكي',
        'shafii': 'الشافعي',
        'hanbali': 'الحنبلي'
      };
      
      const arabicMadhhab = madhhabMapping[madhhab];
      if (!arabicMadhhab) {
        return NextResponse.json({
          status: 'error',
          message: `المذهب ${madhhab} غير متوفر`
        }, { status: 400 });
      }
      
      const result = await madhhabService.getSingleMadhhabResponse(arabicMadhhab, question);
      
      if (result.status === 'error') {
        return NextResponse.json(result, { status: 500 });
      }
      
      return NextResponse.json({
        status: 'success',
        data: {
          answer: result.data?.answer,
          madhhab: madhhab
        }
      });
    } else {
      // إجابة من جميع المذاهب الأربعة
      const result = await madhhabService.getAllMadhahibResponses(question);
      
      if (result.status === 'error') {
        return NextResponse.json(result, { status: 500 });
      }
      
      const combinedAnswer = madhhabService.formatCombinedResponse(result.data!);
      
      return NextResponse.json({
        status: 'success',
        data: {
          answer: combinedAnswer,
          madhhab: 'all',
          individual_responses: result.data
        }
      });
    }

  } catch (error) {
    console.error('Error in chat API:', error);
    return NextResponse.json({
      status: 'error',
      message: 'حدث خطأ أثناء معالجة طلبك'
    }, { status: 500 });
  }
}
