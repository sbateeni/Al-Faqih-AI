from dotenv import load_dotenv
import os
import google.generativeai as genai

# تحميل المتغيرات البيئية
load_dotenv()

# الحصول على مفتاح API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("الرجاء تعيين GEMINI_API_KEY في ملف .env")

def test_api_connection():
    """اختبار الاتصال بـ API"""
    try:
        print("جاري اختبار الاتصال بـ Gemini API...")
        
        # تهيئة الاتصال
        genai.configure(api_key=GEMINI_API_KEY)
        print("✓ تم تهيئة الاتصال بنجاح")
        
        # إنشاء النموذج
        model = genai.GenerativeModel('gemini-pro')
        print("✓ تم إنشاء النموذج بنجاح")
        
        # اختبار إرسال رسالة بسيطة
        response = model.generate_content("السلام عليكم")
        if response and response.text:
            print("✓ تم تلقي استجابة من API بنجاح")
            print("\nمحتوى الاستجابة:")
            print("-" * 50)
            print(response.text)
            print("-" * 50)
        else:
            print("✗ لم يتم تلقي استجابة من API")
        
        return True
        
    except Exception as e:
        print(f"\n✗ حدث خطأ أثناء الاختبار:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return False

def test_complex_prompt():
    """اختبار إرسال prompt معقد"""
    try:
        print("\nجاري اختبار إرسال prompt معقد...")
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # إنشاء prompt معقد
        prompt = """
        بصفتك الإمام الشافعي، كيف تجيب على هذا السؤال:
        ما حكم صلاة الجماعة؟
        
        يرجى تقديم الإجابة متضمنة:
        1. الحكم الشرعي
        2. الأدلة من القرآن والسنة
        3. التعليل والتوضيح
        4. الإجماع أو الخلاف في المسألة
        5. النصائح والإرشادات المتعلقة
        """
        
        response = model.generate_content(prompt)
        if response and response.text:
            print("✓ تم تلقي استجابة للـ prompt المعقد بنجاح")
            print("\nمحتوى الاستجابة:")
            print("-" * 50)
            print(response.text)
            print("-" * 50)
        else:
            print("✗ لم يتم تلقي استجابة للـ prompt المعقد")
        
        return True
        
    except Exception as e:
        print(f"\n✗ حدث خطأ أثناء اختبار الـ prompt المعقد:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return False

def test_chat_history():
    """اختبار المحادثة مع سياق"""
    try:
        print("\nجاري اختبار المحادثة مع سياق...")
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # بدء محادثة جديدة
        chat = model.start_chat(history=[])
        
        # إرسال عدة رسائل متتالية
        messages = [
            "من هو الإمام البخاري؟",
            "متى توفي؟",
            "ما هو أشهر كتبه؟"
        ]
        
        print("\nسجل المحادثة:")
        print("-" * 50)
        
        for msg in messages:
            print(f"\nالسؤال: {msg}")
            response = chat.send_message(msg)
            print(f"الإجابة: {response.text}")
        
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ حدث خطأ أثناء اختبار المحادثة:")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("بدء اختبارات Gemini API")
    print("=" * 50)
    
    # اختبار الاتصال الأساسي
    connection_test = test_api_connection()
    
    if connection_test:
        # اختبار الـ prompt المعقد
        prompt_test = test_complex_prompt()
        
        # اختبار المحادثة
        chat_test = test_chat_history()
        
        # تلخيص النتائج
        print("\nنتائج الاختبارات:")
        print("-" * 50)
        print(f"اختبار الاتصال: {'نجح ✓' if connection_test else 'فشل ✗'}")
        print(f"اختبار الـ prompt المعقد: {'نجح ✓' if prompt_test else 'فشل ✗'}")
        print(f"اختبار المحادثة: {'نجح ✓' if chat_test else 'فشل ✗'}")
    
    print("=" * 50)
    print("انتهت الاختبارات")
    print("=" * 50) 