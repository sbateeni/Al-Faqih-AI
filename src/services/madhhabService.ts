import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from '@/config';
import { MadhhabInfo, MadhhabResponse, ApiResponse } from '@/types';

export class MadhhabService {
  private genAI: GoogleGenerativeAI;
  private model: any;

  constructor(apiKey?: string) {
    const key = apiKey || config.api.gemini.defaultKey;
    this.genAI = new GoogleGenerativeAI(key);
    this.model = this.genAI.getGenerativeModel({ model: config.api.gemini.model });
  }

  // الحصول على معلومات المذاهب
  getMadhahibInfo(): Record<string, MadhhabInfo> {
    return config.madhahib;
  }

  // الحصول على معلومات مذهب واحد
  getMadhhabInfo(madhhabName: string): MadhhabInfo | null {
    const madhahib = this.getMadhahibInfo();
    return madhahib[madhhabName] || null;
  }

  // بناء التوجيه لمذهب معين
  private buildMadhhabPrompt(madhhabInfo: MadhhabInfo, question: string): string {
    return `أنا عالم إسلامي متخصص في المذهب ${madhhabInfo.name}. 
    تحدث باسم المذهب ${madhhabInfo.name} وأجب على السؤال التالي من منظور هذا المذهب:
    
    السؤال: ${question}
    
    ابدأ إجابتك بـ: "أنا المذهب ${madhhabInfo.name}..."
    وتحدث بصيغة المتكلم كأنك المذهب نفسه.
    
    يجب أن تتضمن الإجابة:
    1. تعريف بالمذهب ومؤسسه (${madhhabInfo.founder})
    2. الحكم الشرعي حسب هذا المذهب
    3. الدليل من القرآن أو السنة
    4. أقوال علماء هذا المذهب
    5. المنهجية المميزة لهذا المذهب في الاستنباط
    6. التعليل والحكمة
    
    معلومات إضافية عن المذهب ${madhhabInfo.name}:
    - أشتهر بـ: ${madhhabInfo.methodology}
    - المصادر المعتمدة: ${madhhabInfo.sources.join('، ')}
    - من أبرز علمائه: ${madhhabInfo.scholars.slice(0, 3).join('، ')}
    - ينتشر في: ${madhhabInfo.influence.slice(0, 3).join('، ')}
    
    تأكد من إبراز هذه الخصائص في إجابتك وكيف تؤثر على الحكم الفقهي.`;
  }

  // الحصول على إجابة من مذهب واحد
  async getSingleMadhhabResponse(
    madhhabName: string,
    question: string
  ): Promise<ApiResponse<MadhhabResponse>> {
    try {
      const madhhabInfo = this.getMadhhabInfo(madhhabName);
      if (!madhhabInfo) {
        return {
          status: 'error',
          message: `المذهب ${madhhabName} غير متوفر`,
        };
      }

      const prompt = this.buildMadhhabPrompt(madhhabInfo, question);
      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();

      if (!text) {
        return {
          status: 'error',
          message: `عذراً، لم أتمكن من الحصول على إجابة من المذهب ${madhhabInfo.name}`,
        };
      }

      return {
        status: 'success',
        data: {
          madhhab: madhhabInfo.name,
          answer: text,
          timestamp: new Date().toISOString(),
        },
      };
    } catch (error) {
      console.error(`Error getting response from ${madhhabName}:`, error);
      return {
        status: 'error',
        message: `حدث خطأ أثناء الحصول على إجابة من المذهب ${madhhabName}`,
      };
    }
  }

  // الحصول على إجابات من جميع المذاهب
  async getAllMadhahibResponses(
    question: string
  ): Promise<ApiResponse<Record<string, MadhhabResponse>>> {
    try {
      const madhahib = this.getMadhahibInfo();
      const responses: Record<string, MadhhabResponse> = {};

      for (const [key, madhhabInfo] of Object.entries(madhahib)) {
        try {
          const prompt = this.buildMadhhabPrompt(madhhabInfo, question);
          const result = await this.model.generateContent(prompt);
          const response = await result.response;
          const text = response.text();

          if (text) {
            responses[madhhabInfo.name] = {
              madhhab: madhhabInfo.name,
              answer: text,
              timestamp: new Date().toISOString(),
            };
          } else {
            responses[madhhabInfo.name] = {
              madhhab: madhhabInfo.name,
              answer: `عذراً، لم أتمكن من الحصول على إجابة من المذهب ${madhhabInfo.name}`,
              timestamp: new Date().toISOString(),
            };
          }
        } catch (error) {
          console.error(`Error getting response from ${madhhabInfo.name}:`, error);
          responses[madhhabInfo.name] = {
            madhhab: madhhabInfo.name,
            answer: `حدث خطأ أثناء الحصول على إجابة من المذهب ${madhhabInfo.name}`,
            timestamp: new Date().toISOString(),
          };
        }
      }

      return {
        status: 'success',
        data: responses,
      };
    } catch (error) {
      console.error('Error getting responses from all madhahib:', error);
      return {
        status: 'error',
        message: 'حدث خطأ أثناء الحصول على الإجابات',
      };
    }
  }

  // تنسيق الإجابة المجمعة
  formatCombinedResponse(responses: Record<string, MadhhabResponse>): string {
    let combinedAnswer = '';
    
    for (const [madhhabName, response] of Object.entries(responses)) {
      combinedAnswer += `\n\n${'='.repeat(50)}\n`;
      combinedAnswer += `إجابة المذهب ${madhhabName}\n`;
      combinedAnswer += `${'='.repeat(50)}\n\n`;
      combinedAnswer += response.answer;
    }
    
    return combinedAnswer;
  }
}
