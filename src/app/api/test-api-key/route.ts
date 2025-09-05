import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { TestApiKeyRequest, ApiResponse } from '@/types';
import { config } from '@/config';

export async function POST(request: NextRequest) {
  try {
    const body: TestApiKeyRequest = await request.json();
    const { apiKey } = body;

    if (!apiKey) {
      return NextResponse.json({
        status: 'error',
        message: 'الرجاء إدخال مفتاح API'
      }, { status: 400 });
    }

    try {
      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({ model: config.api.gemini.model });
      
      // اختبار بسيط
      const result = await model.generateContent("قل: مفتاح API يعمل بنجاح");
      const response = await result.response;
      const text = response.text();
      
      if (text) {
        return NextResponse.json({
          status: 'success',
          message: text
        });
      } else {
        return NextResponse.json({
          status: 'error',
          message: 'لم يتم استلام رد من Gemini'
        }, { status: 500 });
      }
    } catch (error) {
      console.error('Error testing API key:', error);
      return NextResponse.json({
        status: 'error',
        message: 'مفتاح API غير صالح أو حدث خطأ'
      }, { status: 400 });
    }

  } catch (error) {
    console.error('Error in test-api-key API:', error);
    return NextResponse.json({
      status: 'error',
      message: 'حدث خطأ أثناء اختبار المفتاح'
    }, { status: 500 });
  }
}
