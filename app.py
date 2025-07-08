from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import google.generativeai as genai
import logging
import traceback

# تهيئة التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        api_key = request.headers.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'status': 'error', 'message': 'API key is required'}), 401
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

        # تهيئة Gemini API بالمفتاح المرسل
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        except Exception as e:
            logger.error(f"Error initializing Gemini: {str(e)}")
            return jsonify({'status': 'error', 'message': 'فشل في تهيئة Gemini API'}), 500

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
        api_key = request.headers.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'status': 'error', 'message': 'API key is required'}), 401
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

        # تهيئة Gemini API بالمفتاح المرسل
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        except Exception as e:
            logger.error(f"Error initializing Gemini: {str(e)}")
            return jsonify({'status': 'error', 'message': 'فشل في تهيئة Gemini API'}), 500
        
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
            [اذكر الأحاديث مع تخريجها]
            
            ### الشرح والمعنى ###
            [اشرح الأحاديث وبيّن معناها]
            
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

        return jsonify({'status': 'success', 'data': answers})

    except Exception as e:
        logger.error(f"Error in ask_quran_sunnah: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء معالجة طلبك'}), 500

@app.route('/test-api-key', methods=['POST'])
def test_api_key():
    try:
        api_key = request.headers.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'status': 'error', 'message': 'API key is required'}), 401
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
            # اختبار بسيط
            response = model.generate_content("قل: مفتاح API يعمل بنجاح")
            if response and response.text:
                return jsonify({'status': 'success', 'message': response.text})
            else:
                return jsonify({'status': 'error', 'message': 'لم يتم استلام رد من Gemini'}), 500
        except Exception as e:
            logger.error(f"Error testing API key: {str(e)}")
            return jsonify({'status': 'error', 'message': 'مفتاح API غير صالح أو حدث خطأ'}), 400
    except Exception as e:
        logger.error(f"Error in test_api_key: {str(e)}")
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء اختبار المفتاح'}), 500

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