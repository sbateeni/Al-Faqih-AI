"""مسارات خاصة بصفحة القرآن والسنة"""

from flask import Blueprint, request, jsonify, render_template
from models.chat import Chat, db
from utils.gemini_helper import GeminiHelper

quran_sunnah_bp = Blueprint('quran_sunnah', __name__)

@quran_sunnah_bp.route('/quran_sunnah')
def quran_sunnah_page():
    """عرض صفحة البحث في القرآن والسنة"""
    return render_template('quran_sunnah.html')

@quran_sunnah_bp.route('/api/quran_sunnah/search', methods=['POST'])
def search_quran_sunnah():
    """البحث في القرآن والسنة"""
    try:
        data = request.get_json()
        query = data.get('query')
        search_type = data.get('type', 'both')  # both, quran, or hadith
        
        if not query:
            return jsonify({'error': 'الرجاء إدخال نص للبحث'}), 400

        # تهيئة Gemini API
        gemini = GeminiHelper.get_instance()
        if not gemini.is_initialized():
            return jsonify({'error': 'لم يتم تهيئة Gemini API. الرجاء إدخال مفتاح API صالح'}), 400

        # إضافة السياق للبحث
        context = f"""أنت باحث متخصص في القرآن والسنة. مهمتك هي:
        1. البحث في {'القرآن الكريم' if search_type == 'quran' else 'الحديث الشريف' if search_type == 'hadith' else 'القرآن الكريم والسنة النبوية'}
        2. إرجاع النصوص المتعلقة بالموضوع مع ذكر المصدر
        3. شرح معاني الآيات والأحاديث بشكل مبسط
        4. ذكر أقوال العلماء في تفسير النصوص إن وجدت
        
        نص البحث هو: {query}
        """
        
        # الحصول على النتائج من النموذج
        response = gemini.generate_text(context)
        
        if not response:
            return jsonify({'error': 'لم نتمكن من الحصول على نتائج. حاول مرة أخرى'}), 500

        # حفظ البحث في قاعدة البيانات
        chat = Chat(
            question=query,
            answer=response,
            chat_type='quran_sunnah'
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            'results': response,
            'chat_id': chat.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500