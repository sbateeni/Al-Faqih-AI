from flask import Blueprint, request, jsonify, current_app
from models.chat import db, Chat
from utils.gemini_helper import GeminiHelper
from prompts.prompts import Prompts
import traceback
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)
gemini = GeminiHelper.get_instance()

def handle_api_error(e):
    """معالجة أخطاء API"""
    error_msg = str(e)
    error_details = traceback.format_exc()
    logger.error(f"Error: {error_msg}\nDetails: {error_details}")

    if "فشل الاتصال" in error_msg or "لا يمكن الاتصال" in error_msg:
        return jsonify({
            'error': 'لا يمكن الاتصال بالخادم. يرجى التحقق من اتصال الإنترنت والمحاولة مرة أخرى.',
            'details': error_msg
        }), 503
    elif "API" in error_msg:
        return jsonify({
            'error': 'حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى لاحقاً.',
            'details': error_msg
        }), 503
    else:
        return jsonify({
            'error': 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.',
            'details': error_msg
        }), 500

@chat_bp.route('/health', methods=['GET'])
def health_check():
    """التحقق من حالة الخادم"""
    try:
        if gemini.initialize_api():
            return jsonify({
                'status': 'healthy',
                'message': 'الخادم يعمل والاتصال بـ API ناجح'
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'message': gemini.get_last_error()
            }), 503
    except Exception as e:
        logger.error(f"Health check error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """معالجة طلبات المحادثة"""
    try:
        # التحقق من الاتصال أولاً
        is_connected, error = gemini.check_connection()
        if not is_connected:
            return jsonify({
                'error': 'خطأ في الاتصال',
                'details': error
            }), 503

        data = request.get_json()
        message = data.get('message')
        scholar = data.get('scholar')
        
        if not message:
            return jsonify({'error': 'الرجاء إدخال رسالة'}), 400
            
        if not scholar:
            return jsonify({'error': 'الرجاء اختيار العالم'}), 400

        #�نشاء البرومبت المناسب للعالم
        prompt = Prompts.get_individual_chat_prompt(scholar, message)
        
        # محاولة الحصول على الرد
        try:
            response = gemini.get_response(prompt)
            
            # حفظ المحادثة في قاعدة البيانات
            try:
                new_chat = Chat(
                    question=message,
                    answer=response,
                    chat_type='individual',
                    scholar=scholar
                )
                db.session.add(new_chat)
                db.session.commit()
            except Exception as db_error:
                logger.error(f"Database error: {str(db_error)}")
                # نستمر حتى لو فشل الحفظ
                pass
                
            return jsonify({'response': response})
        except Exception as e:
            return handle_api_error(e)
            
    except Exception as e:
        return handle_api_error(e)

@chat_bp.route('/chat/individual', methods=['POST'])
def ask_chat():
    """معالجة المحادثات الفردية مع العلماء"""
    try:
        logger.info("Received individual chat request")
        
        if not request.is_json:
            return jsonify({
                'error': 'يجب أن يكون الطلب بتنسيق JSON',
                'details': 'تأكد من إرسال البيانات بتنسيق JSON صحيح'
            }), 400

        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        question = data.get('question')
        scholar = data.get('scholar')
        
        if not question or not scholar:
            return jsonify({
                'error': 'يجب تقديم السؤال والعالم',
                'details': 'تأكد من تحديد السؤال والعالم المطلوب'
            }), 400

        logger.info(f"Processing question for scholar: {scholar}")
        prompt = Prompts.get_individual_chat_prompt(scholar, question)
        response = gemini.get_response(prompt)
        logger.info("Received response from Gemini API")

        # حفظ في قاعدة البيانات
        try:
            new_chat = Chat(
                question=question,
                answer=response,
                chat_type='individual',
                scholar=scholar
            )
            db.session.add(new_chat)
            db.session.commit()
            logger.info("Chat saved to database")
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}\n{traceback.format_exc()}")
            # نستمر حتى لو فشل الحفظ في قاعدة البيانات
            pass

        return jsonify({'response': response})

    except Exception as e:
        logger.error(f"Chat error: {str(e)}\n{traceback.format_exc()}")
        return handle_api_error(e)

@chat_bp.route('/fatwa', methods=['POST'])
def ask_fatwa():
    """معالجة طلبات الفتوى"""
    try:
        # التحقق من الاتصال أولاً
        is_connected, error = gemini.check_connection()
        if not is_connected:
            return jsonify({
                'error': 'خطأ في الاتصال',
                'details': error
            }), 503
            
        data = request.get_json()
        question = data.get('question')
        scholar = data.get('scholar', 'all')
        
        if not question:
            return jsonify({
                'error': 'الرجاء إدخال السؤال',
                'details': 'يجب تقديم سؤال للحصول على فتوى'
            }), 400

        # إنشاء البرومبت المناسب
        prompt = Prompts.get_fatwa_prompt(scholar, question)
        
        # محاولة الحصول على الرد
        try:
            response = gemini.get_response(prompt)
            
            # حفظ الفتوى في قاعدة البيانات
            try:
                new_chat = Chat(
                    question=question,
                    answer=response,
                    chat_type='fatwa',
                    scholar=scholar
                )
                db.session.add(new_chat)
                db.session.commit()
            except Exception as db_error:
                logger.error(f"Database error: {str(db_error)}")
                # نستمر حتى لو فشل الحفظ
                pass
                
            return jsonify({'response': response})
        except Exception as e:
            return handle_api_error(e)
            
    except Exception as e:
        return handle_api_error(e)

@chat_bp.route('/quran-sunnah', methods=['POST'])
def ask_quran_sunnah():
    """معالجة الاستفسارات حول القرآن والسنة"""
    try:
        # التحقق من الاتصال أولاً
        is_connected, error = gemini.check_connection()
        if not is_connected:
            return jsonify({
                'error': 'خطأ في الاتصال',
                'details': error
            }), 503
            
        data = request.get_json()
        question = data.get('question')
        type = data.get('type', 'both')  # quran, hadith, or both
        
        if not question:
            return jsonify({
                'error': 'الرجاء إدخال السؤال',
                'details': 'يجب تقديم سؤال للبحث في القرآن والسنة'
            }), 400

        responses = {}
        
        # الحصول على الإجابة من القرآن إذا كان مطلوباً
        if type in ['quran', 'both']:
            quran_prompt = Prompts.get_quran_prompt(question)
            responses['quran'] = gemini.get_response(quran_prompt)
            
            # حفظ في قاعدة البيانات
            try:
                new_chat = Chat(
                    question=question,
                    answer=responses['quran'],
                    chat_type='quran'
                )
                db.session.add(new_chat)
            except Exception as db_error:
                logger.error(f"Database error (Quran): {str(db_error)}")

        # الحصول على الإجابة من السنة إذا كان مطلوباً
        if type in ['hadith', 'both']:
            hadith_prompt = Prompts.get_hadith_prompt(question)
            responses['hadith'] = gemini.get_response(hadith_prompt)
            
            # حفظ في قاعدة البيانات
            try:
                new_chat = Chat(
                    question=question,
                    answer=responses['hadith'],
                    chat_type='hadith'
                )
                db.session.add(new_chat)
            except Exception as db_error:
                logger.error(f"Database error (Hadith): {str(db_error)}")

        # حفظ التغييرات في قاعدة البيانات
        try:
            db.session.commit()
        except Exception as db_error:
            logger.error(f"Database commit error: {str(db_error)}")
            # نستمر حتى لو فشل الحفظ
            pass
                
        return jsonify(responses)
    except Exception as e:
        return handle_api_error(e) 