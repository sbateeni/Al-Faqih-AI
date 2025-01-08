import google.generativeai as genai
import time
import requests
from config.config import Config

class GeminiHelper:
    _instance = None
    model = None
    _last_error = None
    _is_initialized = False

    @property
    def is_initialized(self):
        """التحقق من حالة التهيئة"""
        return self._is_initialized

    @classmethod
    def get_instance(cls):
        """الحصول على نسخة وحيدة من المساعد"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _check_internet_connection(self):
        """التحقق من اتصال الإنترنت"""
        try:
            # محاولة الاتصال بخادم Google
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.RequestException:
            self._last_error = "لا يمكن الاتصال بالإنترنت. يرجى التحقق من اتصالك بالإنترنت."
            return False

    def _check_api_key(self):
        """التحقق من مفتاح API"""
        if not Config.GEMINI_API_KEY:
            self._last_error = "لم يتم العثور على مفتاح API. يرجى التحقق من ملف .env"
            return False
        return True

    def initialize_api(self):
        """تهيئة الاتصال بـ API"""
        try:
            # التحقق من اتصال الإنترنت أولاً
            if not self._check_internet_connection():
                self._is_initialized = False
                return False

            # التحقق من مفتاح API
            if not self._check_api_key():
                self._is_initialized = False
                return False
            
            # تهيئة الاتصال
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            
            # اختبار الاتصال
            response = self.model.generate_content("اختبار الاتصال")
            if not response or not response.text:
                self._last_error = "لم يتم تلقي استجابة من API. يرجى المحاولة مرة أخرى."
                self._is_initialized = False
                return False
                
            self._last_error = None
            self._is_initialized = True
            return True

        except genai.types.BlockedPromptException:
            self._last_error = "تم حظر المحتوى من قبل API. يرجى تعديل السؤال."
            self._is_initialized = False
            return False
        except genai.types.GenerateContentException:
            self._last_error = "حدث خطأ في إنشاء المحتوى. يرجى المحاولة مرة أخرى."
            self._is_initialized = False
            return False
        except Exception as e:
            self._last_error = f"خطأ غير متوقع: {str(e)}"
            self._is_initialized = False
            return False

    def setup_api(self, api_key=None):
        """إعداد API مع إعادة المحاولة"""
        if api_key:
            Config.GEMINI_API_KEY = api_key
            
        retry_count = 3
        while retry_count > 0:
            if self.initialize_api():
                print("✓ تم تهيئة API بنجاح")
                return True
            print(f"محاولة إعادة الاتصال... ({retry_count} محاولات متبقية)")
            print(f"السبب: {self._last_error}")
            retry_count -= 1
            time.sleep(2)
        
        print("✗ فشل الاتصال بـ API بعد عدة محاولات")
        print(f"آخر خطأ: {self._last_error}")
        return False

    def get_response(self, prompt):
        """الحصول على رد من نموذج Gemini"""
        try:
            print("=== بداية طلب Gemini ===")
            print(f"طول البرومبت: {len(prompt)} حرف")
            
            if not self.is_initialized:
                print("تهيئة نموذج Gemini...")
                self.initialize_api()
                
            if not self.check_internet():
                print("خطأ: لا يوجد اتصال بالإنترنت")
                raise ConnectionError("لا يوجد اتصال بالإنترنت")
                
            print("جاري إرسال الطلب إلى Gemini...")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                print("خطأ: لم يتم استلام رد من Gemini")
                raise ValueError("لم يتم استلام رد من نموذج Gemini")
                
            print("تم استلام الرد بنجاح")
            print(f"طول الرد: {len(response.text)} حرف")
            return response.text
            
        except Exception as e:
            import traceback
            print("=== حدث خطأ في طلب Gemini ===")
            print(f"نوع الخطأ: {type(e).__name__}")
            print(f"رسالة الخطأ: {str(e)}")
            print("تفاصيل الخطأ:")
            print(traceback.format_exc())
            raise

    def get_last_error(self):
        """الحصول على آخر خطأ"""
        return self._last_error or "خطأ غير معروف"
        
    def get_fatwa(self, question, scholar='all'):
        """الحصول على فتوى من العالم المحدد"""
        try:
            print(f"=== طلب فتوى جديد ===")
            print(f"العالم: {scholar}")
            print(f"السؤال: {question}")
            
            if scholar == 'all':
                # تحضير السؤال لكل مذهب
                madhahib = {
                    'hanafi': {
                        'prompt': """أنت الإمام أبو حنيفة النعمان، إمام المذهب الحنفي.
                        السؤال التالي: {question}
                        
                        قدم إجابة شاملة وفق مذهبك مع ذكر:
                        1. الحكم الشرعي
                        2. الأدلة من القرآن والسنة
                        3. تعليل الحكم
                        4. آراء علماء المذهب الحنفي في المسألة""",
                        'scholars': ['أبو حنيفة النعمان', 'أبو يوسف', 'محمد بن الحسن الشيباني']
                    },
                    'maliki': {
                        'prompt': """أنت الإمام مالك بن أنس، إمام المذهب المالكي.
                        السؤال التالي: {question}
                        
                        قدم إجابة شاملة وفق مذهبك مع ذكر:
                        1. الحكم الشرعي
                        2. الأدلة من القرآن والسنة وعمل أهل المدينة
                        3. تعليل الحكم
                        4. آراء علماء المذهب المالكي في المسألة""",
                        'scholars': ['مالك بن أنس', 'ابن القاسم', 'سحنون']
                    },
                    'shafii': {
                        'prompt': """أنت الإمام الشافعي، إمام المذهب الشافعي.
                        السؤال التالي: {question}
                        
                        قدم إجابة شاملة وفق مذهبك مع ذكر:
                        1. الحكم الشرعي
                        2. الأدلة من القرآن والسنة
                        3. تعليل الحكم
                        4. آراء علماء المذهب الشافعي في المسألة""",
                        'scholars': ['محمد بن إدريس الشافعي', 'المزني', 'النووي']
                    },
                    'hanbali': {
                        'prompt': """أنت الإمام أحمد بن حنبل، إمام المذهب الحنبلي.
                        السؤال التالي: {question}
                        
                        قدم إجابة شاملة وفق مذهبك مع ذكر:
                        1. الحكم الشرعي
                        2. الأدلة من القرآن والسنة
                        3. تعليل الحكم
                        4. آراء علماء المذهب الحنبلي في المسألة""",
                        'scholars': ['أحمد بن حنبل', 'ابن قدامة', 'ابن تيمية']
                    }
                }
                
                # الحصول على إجابات من كل مذهب
                responses = {}
                for madhab, info in madhahib.items():
                    prompt = info['prompt'].format(question=question)
                    response = self.get_response(prompt)
                    responses[madhab] = {
                        'text': response,
                        'scholars': info['scholars']
                    }
                
                # إضافة مقارنة وتحليل
                comparison_prompt = f"""بناءً على الإجابات السابقة من المذاهب الأربعة حول السؤال: {question}

                قم بتحليل مقارن يوضح:
                1. نقاط الاتفاق بين المذاهب
                2. نقاط الاختلاف بين المذاهب
                3. سبب الاختلاف إن وجد
                4. الراجح من الأقوال مع التعليل

                قدم التحليل بشكل موضوعي ومختصر."""
                
                comparison = self.get_response(comparison_prompt)
                responses['comparison'] = {
                    'text': comparison,
                    'scholars': ['تحليل مقارن']
                }
                
                return responses
            else:
                # تخصيص الإجابة حسب العالم المختار
                scholar_prompts = {
                    'shafii': 'أنت الإمام الشافعي رحمه الله، تجيب وفق مذهبك',
                    'malik': 'أنت الإمام مالك رحمه الله، تجيب وفق مذهبك',
                    'abu-hanifa': 'أنت الإمام أبو حنيفة رحمه الله، تجيب وفق مذهبك',
                    'ahmad': 'أنت الإمام أحمد بن حنبل رحمه الله، تجيب وفق مذهبك'
                }
                prompt = f"""{scholar_prompts.get(scholar, 'أنت عالم إسلامي متخصص')}
                السؤال التالي: {question}
                
                قدم إجابة شاملة ودقيقة مع ذكر الأدلة من القرآن والسنة."""
                
                response = self.get_response(prompt)
                return {'single': {'text': response, 'scholars': [scholar]}}
            
        except Exception as e:
            import traceback
            print("=== حدث خطأ في get_fatwa ===")
            print(f"نوع الخطأ: {type(e).__name__}")
            print(f"رسالة الخطأ: {str(e)}")
            print("تفاصيل الخطأ:")
            print(traceback.format_exc())
            raise Exception(f"حدث خطأ في الحصول على الفتوى: {str(e)}") 