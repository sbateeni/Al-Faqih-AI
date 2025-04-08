import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time
from prompts.prompts import get_madhhab_prompt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    logger.error("API key not found in .env file")
    raise ValueError("الرجاء تعيين GOOGLE_API_KEY في ملف .env")

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

class MadhhabChat:
    def __init__(self):
        """Initialize the Madhhab chat system"""
        self.model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        self.madhahib = {
            'حنفي': 'أبو حنيفة النعمان',
            'مالكي': 'مالك بن أنس',
            'شافعي': 'محمد بن إدريس الشافعي',
            'حنبلي': 'أحمد بن حنبل'
        }
        
    def get_madhhab_response(self, question, madhhab):
        """Get response from a specific school of thought"""
        try:
            if madhhab == 'quran_sunnah':
                return self.get_quran_sunnah_response(question)
                
            # Use the prompt from prompts.py
            prompt = get_madhhab_prompt(madhhab, question)
            if not prompt:
                return f"عذراً، المذهب {madhhab} غير معروف"
            
            # Add formatting instructions for Quran verses and hadiths
            prompt += """
            
            ملاحظات إضافية للتنسيق:
            - ضع الآيات القرآنية بين قوسين معقوفين {{}} مثل: {{وَالسَّارِقُ وَالسَّارِقَةُ فَاقْطَعُوا أَيْدِيَهُمَا}}
            - ضع الأحاديث النبوية بين قوسين مربعين [] مثل: [عن أبي هريرة رضي الله عنه أن رسول الله صلى الله عليه وسلم قال: لا تقطع يد السارق إلا في ربع دينار فصاعداً]
            """
            
            response = self.model.generate_content(prompt)
            return response.text if response else "عذراً، لم أتمكن من الحصول على إجابة"
            
        except Exception as e:
            logger.error(f"Error in get_madhhab_response: {str(e)}")
            return f"حدث خطأ أثناء الحصول على إجابة من المذهب {madhhab}"

    def get_quran_sunnah_response(self, question):
        """Get response based on Quran and Sunnah evidence"""
        try:
            prompt = f"""
            بسم الله الرحمن الرحيم، والصلاة والسلام على أشرف الأنبياء والمرسلين، سيدنا محمد وعلى آله وصحبه أجمعين.

            مطلوب منك الإجابة على السؤال التالي استناداً إلى القرآن الكريم والسنة النبوية الشريفة:

            السؤال: {question}

            يجب أن تكون إجابتك منظمة بالشكل التالي:

            أولاً: الأدلة من القرآن الكريم
            - اذكر الآيات القرآنية المتعلقة بالموضوع
            - بين وجه الدلالة من كل آية
            - اذكر أقوال المفسرين في معنى الآيات

            ثانياً: الأدلة من السنة النبوية
            - اذكر الأحاديث النبوية الصحيحة المتعلقة بالموضوع
            - بين درجة كل حديث وتخريجه
            - اشرح معنى الأحاديث من كتب الشروح المعتمدة

            ثالثاً: الإجماع
            - اذكر ما ورد من إجماع العلماء في المسألة إن وجد

            رابعاً: الاستنباط والفوائد
            - استنبط الأحكام والفوائد من النصوص
            - اربط بين الأدلة وبين بعضها
            - وضح كيف تتكامل الأدلة في بيان الحكم

            ملاحظات للتنسيق:
            - ضع الآيات القرآنية بين قوسين معقوفين {{}} مثل: {{وَالسَّارِقُ وَالسَّارِقَةُ فَاقْطَعُوا أَيْدِيَهُمَا}}
            - ضع الأحاديث النبوية بين قوسين مربعين [] مثل: [عن أبي هريرة رضي الله عنه أن رسول الله صلى الله عليه وسلم قال: لا تقطع يد السارق إلا في ربع دينار فصاعداً]
            """

            response = self.model.generate_content(prompt)
            return response.text if response else "عذراً، لم أتمكن من الحصول على إجابة"

        except Exception as e:
            logger.error(f"Error in get_quran_sunnah_response: {str(e)}")
            return "حدث خطأ أثناء الحصول على الإجابة من القرآن والسنة"

    def get_all_madhahib_responses(self, question):
        """Get responses from all four schools of thought"""
        responses = {}
        for madhhab in self.madhahib.keys():
            print(f"\nجاري الحصول على إجابة من المذهب {madhhab}...")
            response = self.get_madhhab_response(question, madhhab)
            responses[madhhab] = response
            time.sleep(2)  # Add delay between requests
        return responses

def main():
    print("=" * 50)
    print("نظام المحادثة مع المذاهب الأربعة")
    print("=" * 50)
    
    chat_system = MadhhabChat()
    
    while True:
        print("\nاختر أحد الخيارات التالية:")
        print("1. سؤال لجميع المذاهب")
        print("2. سؤال لمذهب معين")
        print("3. سؤال للقرآن والسنة")
        print("4. خروج")
        
        choice = input("\nاختيارك: ")
        
        if choice == "1":
            question = input("\nأدخل سؤالك: ")
            print("\nجاري جمع الإجابات من جميع المذاهب...")
            responses = chat_system.get_all_madhahib_responses(question)
            
            print("\nالإجابات:")
            print("=" * 50)
            for madhhab, response in responses.items():
                print(f"\nالمذهب {madhhab}:")
                print("-" * 30)
                print(response)
                print("=" * 50)
                
        elif choice == "2":
            print("\nاختر المذهب:")
            for i, madhhab in enumerate(chat_system.madhahib.keys(), 1):
                print(f"{i}. {madhhab}")
            
            madhhab_choice = input("\nاختيارك: ")
            try:
                madhhab_index = int(madhhab_choice) - 1
                selected_madhhab = list(chat_system.madhahib.keys())[madhhab_index]
                question = input("\nأدخل سؤالك: ")
                
                print(f"\nجاري الحصول على إجابة من المذهب {selected_madhhab}...")
                response = chat_system.get_madhhab_response(question, selected_madhhab)
                
                print("\nالإجابة:")
                print("=" * 50)
                print(response)
                print("=" * 50)
                
            except (ValueError, IndexError):
                print("اختيار غير صحيح")
                
        elif choice == "3":
            question = input("\nأدخل سؤالك: ")
            print("\nجاري البحث في القرآن والسنة...")
            response = chat_system.get_quran_sunnah_response(question)
            
            print("\nالإجابة:")
            print("=" * 50)
            print(response)
            print("=" * 50)
                
        elif choice == "4":
            print("\nشكراً لاستخدام نظام المحادثة مع المذاهب الأربعة")
            break
            
        else:
            print("اختيار غير صحيح، الرجاء المحاولة مرة أخرى")

if __name__ == "__main__":
    main() 