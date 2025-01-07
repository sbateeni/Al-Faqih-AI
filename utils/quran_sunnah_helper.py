"""مساعد للتعامل مع طلبات القرآن والسنة"""

from utils.gemini_helper import GeminiHelper
from prompts.quran_sunnah_prompts import get_prompt

class QuranSunnahHelper:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """الحصول على نسخة وحيدة من المساعد"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """تهيئة المساعد"""
        self.gemini = GeminiHelper.get_instance()
    
    def get_quran_tafsir(self, text):
        """الحصول على تفسير آية أو نص قرآني"""
        try:
            print("=== طلب تفسير قرآني ===")
            print(f"النص: {text}")
            prompt = get_prompt('quran_tafsir', text)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في الحصول على التفسير: {str(e)}")
            raise
    
    def get_hadith_explanation(self, text):
        """الحصول على شرح حديث"""
        try:
            print("=== طلب شرح حديث ===")
            print(f"النص: {text}")
            prompt = get_prompt('hadith_explanation', text)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في الحصول على شرح الحديث: {str(e)}")
            raise
    
    def search_quran(self, topic):
        """البحث في القرآن عن موضوع معين"""
        try:
            print("=== طلب بحث في القرآن ===")
            print(f"الموضوع: {topic}")
            prompt = get_prompt('quran_search', topic)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في البحث في القرآن: {str(e)}")
            raise
    
    def search_hadith(self, topic):
        """البحث في الأحاديث عن موضوع معين"""
        try:
            print("=== طلب بحث في الأحاديث ===")
            print(f"الموضوع: {topic}")
            prompt = get_prompt('hadith_search', topic)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في البحث في الأحاديث: {str(e)}")
            raise
    
    def analyze_arabic(self, text):
        """تحليل نص عربي (إعراب وبلاغة)"""
        try:
            print("=== طلب تحليل لغوي ===")
            print(f"النص: {text}")
            prompt = get_prompt('arabic_language', text)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في التحليل اللغوي: {str(e)}")
            raise
    
    def compare_texts(self, topic):
        """مقارنة بين النصوص القرآنية والأحاديث في موضوع معين"""
        try:
            print("=== طلب مقارنة نصوص ===")
            print(f"الموضوع: {topic}")
            prompt = get_prompt('comparison', topic)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في مقارنة النصوص: {str(e)}")
            raise
    
    def get_comprehensive_analysis(self, text):
        """تحليل شامل يجمع بين جميع أنواع التحليل"""
        try:
            print("=== طلب تحليل شامل ===")
            print(f"النص: {text}")
            prompt = get_prompt('comprehensive', text)
            print("تم تجهيز البرومبت")
            return self.gemini.get_response(prompt)
        except Exception as e:
            print(f"خطأ في التحليل الشامل: {str(e)}")
            raise 