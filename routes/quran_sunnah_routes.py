"""مسارات خاصة بصفحة القرآن والسنة"""

from flask import Blueprint, request, jsonify
from utils.quran_sunnah_helper import QuranSunnahHelper
from routes.history_routes import save_to_history

quran_sunnah_bp = Blueprint('quran_sunnah', __name__)

@quran_sunnah_bp.route('/api/quran/tafsir', methods=['POST'])
def get_tafsir():
    """الحصول على تفسير آية"""
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': 'الرجاء إدخال النص'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        response = helper.get_quran_tafsir(text)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/api/hadith/explain', methods=['POST'])
def explain_hadith():
    """الحصول على شرح حديث"""
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': 'الرجاء إدخال النص'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        response = helper.get_hadith_explanation(text)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/api/quran/search', methods=['POST'])
def search_quran():
    """البحث في القرآن"""
    try:
        topic = request.json.get('topic')
        if not topic:
            return jsonify({'error': 'الرجاء إدخال موضوع البحث'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        response = helper.search_quran(topic)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/api/hadith/search', methods=['POST'])
def search_hadith():
    """البحث في الأحاديث"""
    try:
        topic = request.json.get('topic')
        if not topic:
            return jsonify({'error': 'الرجاء إدخال موضوع البحث'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        response = helper.search_hadith(topic)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/api/arabic/analyze', methods=['POST'])
def analyze_arabic():
    """تحليل نص عربي"""
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': 'الرجاء إدخال النص'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        response = helper.analyze_arabic(text)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/api/texts/compare', methods=['POST'])
def compare_texts():
    """مقارنة النصوص"""
    try:
        topic = request.json.get('topic')
        if not topic:
            return jsonify({'error': 'الرجاء إدخال موضوع المقارنة'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        response = helper.compare_texts(topic)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/ask_quran_sunnah', methods=['POST'])
def ask_quran_sunnah():
    """معالجة جميع طلبات القرآن والسنة"""
    try:
        print("=== بداية معالجة طلب القرآن والسنة ===")
        data = request.json
        print(f"البيانات المستلمة: {data}")
        
        if not data:
            print("خطأ: لم يتم استلام بيانات")
            return jsonify({'error': 'الرجاء إدخال البيانات المطلوبة'}), 400
            
        request_type = data.get('type')
        text = data.get('text')
        category = data.get('category')  # تصنيف السؤال (اختياري)
        
        print(f"نوع الطلب: {request_type}")
        print(f"النص المدخل: {text}")
        print(f"التصنيف: {category}")
        
        if not request_type or not text:
            print("خطأ: نوع الطلب أو النص غير موجود")
            return jsonify({'error': 'الرجاء إدخال نوع الطلب والنص'}), 400
            
        helper = QuranSunnahHelper.get_instance()
        print("تم إنشاء مساعد القرآن والسنة بنجاح")
        
        # تحديد نوع الطلب وتوجيهه للدالة المناسبة
        handlers = {
            'quran_tafsir': helper.get_quran_tafsir,
            'hadith_explanation': helper.get_hadith_explanation,
            'quran_search': helper.search_quran,
            'hadith_search': helper.search_hadith,
            'arabic_language': helper.analyze_arabic,
            'comparison': helper.compare_texts,
            'comprehensive': helper.get_comprehensive_analysis
        }
        
        handler = handlers.get(request_type)
        if not handler:
            print(f"خطأ: نوع الطلب غير معروف: {request_type}")
            return jsonify({'error': f'نوع الطلب غير معروف: {request_type}'}), 400
            
        print(f"جاري معالجة الطلب باستخدام: {handler.__name__}")
        response = handler(text)
        print("تم الحصول على الرد بنجاح")
        print(f"طول الرد: {len(response) if response else 0} حرف")
        
        # حفظ السؤال والإجابة في السجل
        history_item = save_to_history(text, response, request_type, category)
        if history_item:
            print(f"تم حفظ السؤال في السجل برقم: {history_item.id}")
        
        return jsonify({
            'response': response,
            'history_id': history_item.id if history_item else None
        })
        
    except Exception as e:
        import traceback
        print("=== حدث خطأ في معالجة طلب القرآن والسنة ===")
        print(f"نوع الخطأ: {type(e).__name__}")
        print(f"رسالة الخطأ: {str(e)}")
        print("تفاصيل الخطأ:")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500 