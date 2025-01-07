from flask import Blueprint, render_template, request, jsonify
from utils.gemini_helper import GeminiHelper

page_bp = Blueprint('pages', __name__)

@page_bp.route('/')
def home():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@page_bp.route('/chat')
def chat():
    """صفحة المحادثة الفردية"""
    return render_template('chat.html')

@page_bp.route('/fatwa')
def fatwa():
    """صفحة الفتوى"""
    return render_template('fatwa.html')

@page_bp.route('/quran-sunnah')
def quran_sunnah():
    """صفحة القرآن والسنة"""
    return render_template('quran_sunnah.html')

@page_bp.route('/ask_fatwa', methods=['POST'])
def ask_fatwa():
    """معالجة طلب الفتوى"""
    try:
        print("=== بداية معالجة طلب الفتوى ===")
        
        # طباعة بيانات الطلب
        print(f"نوع الطلب: {request.content_type}")
        print(f"بيانات الطلب: {request.get_data(as_text=True)}")
        
        question = request.json.get('question')
        scholar = request.json.get('scholar', 'all')
        
        print(f"السؤال: {question}")
        print(f"العالم المختار: {scholar}")
        
        if not question:
            print("خطأ: لم يتم إدخال سؤال")
            return jsonify({'error': 'الرجاء إدخال السؤال'}), 400
            
        gemini = GeminiHelper.get_instance()
        print("تم إنشاء نسخة من GeminiHelper")
        
        responses = gemini.get_fatwa(question, scholar)
        
        if scholar == 'all':
            print(f"تم استلام الردود من المذاهب المختلفة")
            return jsonify({
                'responses': responses,
                'type': 'multiple'
            })
        else:
            print(f"تم استلام الرد من العالم المختار")
            return jsonify({
                'response': responses['single']['text'],
                'type': 'single'
            })
            
    except Exception as e:
        import traceback
        print("=== حدث خطأ ===")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        print("تفاصيل الخطأ:")
        print(traceback.format_exc())
        return jsonify({'error': f'حدث خطأ في معالجة الطلب: {str(e)}'}), 500 