from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import traceback

# تهيئة التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# تحميل المتغيرات البيئية
load_dotenv()

# تهيئة Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error("API key not found in .env file")
    raise ValueError("الرجاء تعيين GOOGLE_API_KEY في ملف .env")

logger.info(f"API Key found: {api_key[:5]}...{api_key[-5:]}")

# تهيئة النموذج
try:
    logger.info("Configuring API with provided key...")
    genai.configure(api_key=api_key)
    
    logger.info("Initializing Gemini model...")
    model = genai.GenerativeModel('models/gemini-2.0-flash-001')
    logger.info("Model initialized successfully")
except Exception as e:
    logger.error(f"Error initializing model: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

# تهيئة تطبيق Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

@app.route('/favicon.ico')
def favicon():
    """خدمة أيقونة الموقع"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return render_template('home.html')

@app.route('/madhahib')
def madhahib():
    """صفحة المذاهب الأربعة"""
    return render_template('madhahib.html')

@app.route('/quran-sunnah')
def quran_sunnah():
    """صفحة القرآن والسنة"""
    return render_template('quran_sunnah.html')

@app.route('/chat', methods=['POST'])
def chat():
    """معالجة المحادثة"""
    try:
        data = request.get_json()
        question = data.get('question')
        madhhab = data.get('madhhab')

        if not question:
            return jsonify({
                'status': 'error',
                'message': 'الرجاء إدخال سؤال'
            }), 400

        logger.info(f"Processing chat request. Question: {question}, Madhhab: {madhhab}")

        # بناء النص التوجيهي
        if madhhab:
            prompt = f"""أنت عالم إسلامي متخصص في المذهب {madhhab}. 
            الرجاء الإجابة على السؤال التالي وفقاً لهذا المذهب:
            
            السؤال: {question}
            
            يجب أن تتضمن الإجابة:
            1. الحكم الشرعي
            2. الدليل من القرآن أو السنة إن وجد
            3. أقوال علماء المذهب {madhhab}
            4. التعليل والحكمة من الحكم"""
        else:
            prompt = f"""الرجاء الإجابة على السؤال التالي من منظور إسلامي عام:
            
            السؤال: {question}
            
            يجب أن تتضمن الإجابة:
            1. الحكم الشرعي
            2. الدليل من القرآن أو السنة إن وجد
            3. آراء العلماء المعتبرين
            4. التعليل والحكمة من الحكم"""

        # الحصول على الإجابة من Gemini
        logger.info("Sending prompt to model...")
        response = model.generate_content(prompt)
        
        if response and response.text:
            logger.info("Successfully received response from model")
            return jsonify({
                'status': 'success',
                'data': {
                    'answer': response.text,
                    'madhhab': madhhab
                }
            })
        else:
            logger.warning("Received empty response from model")
            return jsonify({
                'status': 'error',
                'message': 'لم يتم استلام إجابة من النموذج'
            }), 500

    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': 'حدث خطأ أثناء معالجة طلبك'
        }), 500

@app.route('/ask-quran-sunnah', methods=['POST'])
def ask_quran_sunnah():
    """معالجة الأسئلة المتعلقة بالقرآن والسنة"""
    try:
        data = request.get_json()
        question = data.get('question')
        search_type = data.get('type', 'both')  # 'quran', 'hadith', or 'both'

        if not question:
            return jsonify({
                'status': 'error',
                'message': 'الرجاء إدخال سؤال'
            }), 400

        logger.info(f"Processing Quran/Sunnah request. Question: {question}, Type: {search_type}")
        answers = {}
        
        # البحث في القرآن
        if search_type in ['quran', 'both']:
            logger.info("Searching Quran...")
            quran_prompt = f"""أنت عالم متخصص في القرآن الكريم وتفسيره.
            مهمتك هي البحث عن إجابة للسؤال التالي من القرآن الكريم.
            يجب أن تكون إجابتك دقيقة وموثقة ومنظمة حسب العناصر المطلوبة.
            
            السؤال: {question}
            
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
            [اذكر المصادر التي رجعت إليها]"""
            
            try:
                quran_response = model.generate_content(quran_prompt)
                if quran_response and quran_response.text:
                    logger.info("Successfully received Quran response")
                    # تنظيف وتنسيق النص
                    formatted_response = quran_response.text.strip()
                    answers['quran'] = {
                        'full_response': formatted_response,
                        'sections': parse_response_sections(formatted_response)
                    }
                    logger.info(f"Parsed Quran sections: {list(answers['quran']['sections'].keys())}")
                else:
                    logger.warning("Received empty Quran response")
            except Exception as e:
                logger.error(f"Error generating Quran response: {str(e)}")
                answers['quran_error'] = str(e)

        # البحث في السنة
        if search_type in ['hadith', 'both']:
            logger.info("Searching Hadith...")
            hadith_prompt = f"""أنت عالم متخصص في الحديث النبوي وعلومه.
            مهمتك هي البحث عن إجابة للسؤال التالي من السنة النبوية.
            يجب أن تكون إجابتك دقيقة وموثقة ومنظمة حسب العناصر المطلوبة.
            
            السؤال: {question}
            
            قم بتنسيق إجابتك بالضبط كما يلي، مع الحفاظ على العناوين كما هي:
            
            ### الأحاديث المتعلقة بالموضوع ###
            [اذكر الأحاديث كاملة مع تخريجها ودرجتها]
            
            ### شرح الأحاديث ###
            [اشرح معاني الأحاديث من كتب الشروح المعتمدة مثل فتح الباري، شرح النووي]
            
            ### الأحكام المستنبطة ###
            [اذكر الأحكام الشرعية المستنبطة من الأحاديث]
            
            ### التطبيق المعاصر ###
            [اربط الأحاديث بالواقع المعاصر]
            
            ### المصادر ###
            [اذكر المصادر التي رجعت إليها]"""
            
            try:
                hadith_response = model.generate_content(hadith_prompt)
                if hadith_response and hadith_response.text:
                    logger.info("Successfully received Hadith response")
                    # تنظيف وتنسيق النص
                    formatted_response = hadith_response.text.strip()
                    answers['hadith'] = {
                        'full_response': formatted_response,
                        'sections': parse_response_sections(formatted_response)
                    }
                    logger.info(f"Parsed Hadith sections: {list(answers['hadith']['sections'].keys())}")
                else:
                    logger.warning("Received empty Hadith response")
            except Exception as e:
                logger.error(f"Error generating Hadith response: {str(e)}")
                answers['hadith_error'] = str(e)

        if answers:
            # تحقق من وجود أخطاء
            errors = {}
            if 'quran_error' in answers:
                errors['quran'] = answers.pop('quran_error')
            if 'hadith_error' in answers:
                errors['hadith'] = answers.pop('hadith_error')
            
            response_data = {
                'status': 'success',
                'data': answers,
                'question': question,
                'search_type': search_type
            }
            
            if errors:
                response_data['errors'] = errors
            
            logger.info(f"Sending response with data keys: {list(answers.keys())}")
            return jsonify(response_data)
        else:
            logger.warning("No answers found")
            return jsonify({
                'status': 'error',
                'message': 'لم يتم العثور على إجابات في المصادر المطلوبة'
            }), 500

    except Exception as e:
        logger.error(f"Error in ask_quran_sunnah: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': 'حدث خطأ أثناء معالجة طلبك'
        }), 500

@app.route('/test-api-key', methods=['POST'])
def test_api_key():
    """فحص صلاحية مفتاح Gemini API المرسل من المستخدم"""
    try:
        data = request.get_json()
        user_api_key = data.get('api_key', '').strip()
        if not user_api_key:
            return jsonify({'status': 'error', 'message': 'يرجى إدخال مفتاح API'}), 400
        try:
            genai.configure(api_key=user_api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
            prompt = "Say 'نجح الاتصال' in Arabic."
            response = model.generate_content(prompt)
            if response and response.text and 'نجح الاتصال' in response.text:
                return jsonify({'status': 'success', 'message': 'تم التحقق من المفتاح بنجاح'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'لم يتم التحقق من المفتاح. يرجى التأكد من صحته.'}), 400
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'فشل التحقق من المفتاح: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء معالجة الطلب'}), 500

def parse_response_sections(response_text):
    """تقسيم النص إلى أقسام باستخدام العناوين"""
    sections = {}
    current_section = None
    current_content = []
    
    for line in response_text.split('\n'):
        line = line.strip()
        if line.startswith('###') and line.endswith('###'):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
                current_content = []
            current_section = line.strip('# ').strip()
        elif current_section and line:
            current_content.append(line)
    
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

if __name__ == '__main__':
    app.run(debug=True) 