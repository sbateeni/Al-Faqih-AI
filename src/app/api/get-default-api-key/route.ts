import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from '@/config';

export async function GET(request: NextRequest) {
  try {
    // No default key available - users must provide their own
    return NextResponse.json({
      status: 'error',
      message: 'لا يوجد مفتاح افتراضي. يرجى إدخال مفتاح API الخاص بك في صفحة الإعدادات.',
      requiresUserKey: true
    });

  } catch (error) {
    console.error('Error in get-default-api-key:', error);
    return NextResponse.json({
      status: 'error',
      message: 'حدث خطأ في النظام'
    }, { status: 500 });
  }
}
