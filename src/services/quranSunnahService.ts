import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from '@/config';
import { QuranSunnahResponse, ApiResponse } from '@/types';

export class QuranSunnahService {
  private genAI: GoogleGenerativeAI;
  private model: any;

  constructor(apiKey?: string) {
    const key = apiKey || config.api.gemini.defaultKey;
    this.genAI = new GoogleGenerativeAI(key);
    this.model = this.genAI.getGenerativeModel({ model: config.api.gemini.model });
  }

  // البحث في القرآن الكريم
  private buildQuranPrompt(question: string): string {
    return `أنت عالم متخصص في القرآن الكريم وتفسيره.
    مهمتك هي البحث عن إجابة للسؤال التالي من القرآن الكريم.
    يجب أن تكون إجابتك دقيقة وموثقة ومنظمة حسب العناصر المطلوبة.
    
    السؤال: ${question}
    
    قم بتنسيق إجابتك بالضبط كما يلي، مع الحفاظ على العناوين كما هي:
    
    ### الآيات المتعلقة بالموضوع ###
    [اذكر الآيات مع أرقامها وأسماء السور]
    
    ### التفسير ###
    [اذكر تفسير الآيات من المصادر المعتمدة مثل تفسير ابن كثير، الطبري، القرطبي]
    
    ### الأحكام المستنبطة ###
    [اذكر الأحكام الشرعية المستنبطة من الآيات]
    
    ### التطبيق المعاصر ###
    [اربط الآيات بالواقع المعاصر]
    
    ### المصادر ###
    [اذكر المصادر التي رجعت إليها]`;
  }

  // البحث في السنة النبوية
  private buildHadithPrompt(question: string): string {
    return `أنت عالم متخصص في الحديث النبوي وعلومه.
    مهمتك هي البحث عن إجابة للسؤال التالي من السنة النبوية.
    يجب أن تكون إجابتك دقيقة وموثقة ومنظمة حسب العناصر المطلوبة.
    
    السؤال: ${question}
    
    قم بتنسيق إجابتك بالضبط كما يلي، مع الحفاظ على العناوين كما هي:
    
    ### الأحاديث المتعلقة بالموضوع ###
    [اذكر الأحاديث مع تخريجها]
    
    ### الشرح والمعنى ###
    [اشرح الأحاديث وبيّن معناها]
    
    ### الأحكام المستنبطة ###
    [اذكر الأحكام الشرعية المستنبطة من الأحاديث]
    
    ### التطبيق المعاصر ###
    [اربط الأحاديث بالواقع المعاصر]
    
    ### المصادر ###
    [اذكر المصادر التي رجعت إليها]`;
  }

  // تقسيم النص إلى أقسام
  private parseResponseSections(responseText: string): Record<string, string> {
    const sections: Record<string, string> = {};
    let currentSection: string | null = null;
    const currentContent: string[] = [];
    
    for (const line of responseText.split('\n')) {
      const trimmedLine = line.trim();
      if (trimmedLine.startsWith('###') && trimmedLine.endsWith('###')) {
        if (currentSection) {
          sections[currentSection] = currentContent.join('\n').trim();
        }
        currentSection = trimmedLine.replace(/###/g, '').trim();
        currentContent.length = 0;
      } else if (currentSection && trimmedLine) {
        currentContent.push(trimmedLine);
      }
    }
    
    if (currentSection && currentContent.length > 0) {
      sections[currentSection] = currentContent.join('\n').trim();
    }
    
    return sections;
  }

  // البحث في القرآن
  async searchQuran(question: string): Promise<ApiResponse<QuranSunnahResponse['quran']>> {
    try {
      const prompt = this.buildQuranPrompt(question);
      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();

      if (!text) {
        return {
          status: 'error',
          message: 'لم يتم العثور على نتائج في القرآن الكريم',
        };
      }

      const sections = this.parseResponseSections(text);
      
      return {
        status: 'success',
        data: {
          full_response: text,
          sections,
        },
      };
    } catch (error) {
      console.error('Error searching Quran:', error);
      return {
        status: 'error',
        message: 'حدث خطأ أثناء البحث في القرآن الكريم',
      };
    }
  }

  // البحث في السنة
  async searchHadith(question: string): Promise<ApiResponse<QuranSunnahResponse['hadith']>> {
    try {
      const prompt = this.buildHadithPrompt(question);
      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();

      if (!text) {
        return {
          status: 'error',
          message: 'لم يتم العثور على نتائج في السنة النبوية',
        };
      }

      const sections = this.parseResponseSections(text);
      
      return {
        status: 'success',
        data: {
          full_response: text,
          sections,
        },
      };
    } catch (error) {
      console.error('Error searching Hadith:', error);
      return {
        status: 'error',
        message: 'حدث خطأ أثناء البحث في السنة النبوية',
      };
    }
  }

  // البحث في القرآن والسنة معاً
  async searchBoth(question: string): Promise<ApiResponse<QuranSunnahResponse>> {
    try {
      const [quranResult, hadithResult] = await Promise.allSettled([
        this.searchQuran(question),
        this.searchHadith(question),
      ]);

      const response: QuranSunnahResponse = {};

      if (quranResult.status === 'fulfilled' && quranResult.value.status === 'success') {
        response.quran = quranResult.value.data;
      } else if (quranResult.status === 'rejected') {
        response.quran_error = quranResult.reason.message;
      }

      if (hadithResult.status === 'fulfilled' && hadithResult.value.status === 'success') {
        response.hadith = hadithResult.value.data;
      } else if (hadithResult.status === 'rejected') {
        response.hadith_error = hadithResult.reason.message;
      }

      return {
        status: 'success',
        data: response,
      };
    } catch (error) {
      console.error('Error searching both Quran and Hadith:', error);
      return {
        status: 'error',
        message: 'حدث خطأ أثناء البحث',
      };
    }
  }
}
