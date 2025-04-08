import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# تحميل المتغيرات البيئية
load_dotenv()

# الحصول على مفتاح API
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    logger.error("API key not found in .env file")
    raise ValueError("الرجاء تعيين GOOGLE_API_KEY في ملف .env")

logger.info(f"API Key found: {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}")

def list_available_models():
    """عرض النماذج المتاحة"""
    try:
        logger.info("Configuring API with provided key...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        logger.info("Fetching available models...")
        models = genai.list_models()
        
        if not models:
            logger.warning("No models were returned from the API")
            print("\n✗ لم يتم العثور على نماذج متاحة")
            return None
            
        print("\nالنماذج المتاحة:")
        print("-" * 50)
        for model in models:
            logger.info(f"Found model: {model.name}")
            print(f"اسم النموذج: {model.name}")
            print(f"الوصف: {model.description}")
            print(f"الطرق المدعومة: {model.supported_generation_methods}")
            print("-" * 30)
        return models
    except Exception as e:
        logger.error(f"Error while listing models: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"\n✗ حدث خطأ أثناء التحقق من النماذج:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return None

def test_api_connection():
    """اختبار الاتصال بواجهة برمجة التطبيقات"""
    try:
        logger.info("Starting API connection test...")
        print("\nجاري اختبار الاتصال...")
        
        # تهيئة الاتصال
        logger.info("Initializing API connection...")
        genai.configure(api_key=GEMINI_API_KEY)
        print("✓ تم تهيئة الاتصال بنجاح")
        
        # البحث عن نموذج Gemini 2.0 Flash
        logger.info("Looking for Gemini 2.0 Flash model...")
        model_name = 'models/gemini-2.0-flash-001'
        models = genai.list_models()
        model_found = any(model.name == model_name for model in models)
        
        if not model_found:
            logger.error(f"Model {model_name} not found in available models")
            print(f"✗ لم يتم العثور على نموذج {model_name}")
            return False
            
        logger.info(f"Model {model_name} found, initializing...")
        model = genai.GenerativeModel(model_name)
        
        # اختبار توليد نص بسيط
        prompt = "Say 'Hello, API test successful!' in Arabic"
        logger.info(f"Testing model with prompt: {prompt}")
        
        response = model.generate_content(prompt)
        if response and response.text:
            logger.info("Successfully received response from model")
            print("✓ تم اختبار النموذج بنجاح")
            print(f"استجابة النموذج: {response.text}")
            return True
        else:
            logger.warning("Received empty response from model")
            print("✗ لم يتم استلام استجابة من النموذج")
            return False
            
    except Exception as e:
        logger.error(f"API connection test failed: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"\n✗ فشل اختبار الاتصال:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return False

def test_complex_prompt():
    """اختبار إرسال نص معقد"""
    try:
        logger.info("Starting complex prompt test...")
        print("\nاختبار إرسال نص معقد...")
        
        model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        logger.info("Model initialized for complex prompt test")
        
        prompt = """
        قم بتحليل النص التالي وتحديد:
        1. الموضوع الرئيسي
        2. الأفكار الفرعية
        3. الخلاصة
        
        النص: العلم نور يضيء طريق الإنسان نحو التقدم والازدهار. وهو سلاح قوي في مواجهة الجهل والتخلف.
        يساعد العلم في حل المشكلات وتطوير المجتمعات وتحسين حياة البشر.
        """
        
        logger.info("Sending complex prompt to model...")
        response = model.generate_content(prompt)
        
        if response and response.text:
            logger.info("Successfully received response for complex prompt")
            print("✓ تم تلقي استجابة للنص المعقد بنجاح")
            print("\nالاستجابة:")
            print("-" * 50)
            print(response.text)
            print("-" * 50)
            return True
        else:
            logger.warning("Received empty response for complex prompt")
            print("✗ لم يتم تلقي استجابة للنص المعقد")
            return False
            
    except Exception as e:
        logger.error(f"Complex prompt test failed: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"\n✗ فشل اختبار النص المعقد:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return False

def test_chat_history():
    """اختبار المحادثة مع سجل المحادثة"""
    try:
        logger.info("Starting chat history test...")
        print("\nاختبار المحادثة مع سجل المحادثة...")
        
        model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        chat = model.start_chat()
        logger.info("Chat session initialized")
        
        messages = [
            "مرحباً، كيف حالك؟",
            "ما هو موضوع تخصصك؟",
            "هل يمكنك مساعدتي في فهم موضوع معين؟"
        ]
        
        for msg in messages:
            logger.info(f"Sending message to chat: {msg}")
            response = chat.send_message(msg)
            
            if response and response.text:
                logger.info("Successfully received chat response")
                print(f"\nالرسالة: {msg}")
                print(f"الاستجابة: {response.text}")
            else:
                logger.warning(f"Received empty response for message: {msg}")
                print(f"✗ لم يتم تلقي استجابة للرسالة: {msg}")
                return False
        
        logger.info("Chat history test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Chat history test failed: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"\n✗ فشل اختبار المحادثة:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("بدء اختبارات Gemini API")
    print("=" * 50)
    
    # عرض النماذج المتاحة أولاً
    models = list_available_models()
    if not models:
        print("✗ فشل في الحصول على قائمة النماذج")
        exit(1)
        
    # إضافة تأخير بين الاختبارات
    connection_test = test_api_connection()
    if connection_test:
        time.sleep(2)  # تأخير قبل اختبار الـ prompt المعقد
        prompt_test = test_complex_prompt()
        
        if prompt_test:
            time.sleep(2)  # تأخير قبل اختبار المحادثة
            chat_test = test_chat_history()
        
        # تلخيص النتائج
        print("\nنتائج الاختبارات:")
        print("-" * 50)
        print(f"اختبار الاتصال: {'نجح ✓' if connection_test else 'فشل ✗'}")
        print(f"اختبار الـ prompt المعقد: {'نجح ✓' if prompt_test else 'فشل ✗'}")
        if 'chat_test' in locals():
            print(f"اختبار المحادثة: {'نجح ✓' if chat_test else 'فشل ✗'}")
    
    print("=" * 50)
    print("انتهت الاختبارات")
    print("=" * 50) 