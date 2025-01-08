"""مسارات خاصة بصفحة القرآن والسنة"""

from flask import Blueprint, request, jsonify
from utils.gemini_helper import GeminiHelper
from routes.history_routes import save_to_history

quran_sunnah_bp = Blueprint('quran_sunnah', __name__)

@quran_sunnah_bp.route('/api/quran-sunnah', methods=['POST'])
def ask_quran_sunnah():
    """معالجة الأسئلة المتعلقة بالقرآن والسنة"""
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'الرجاء إدخال السؤال'}), 400
            
        gemini = GeminiHelper.get_instance()
        response = gemini.get_quran_sunnah_answer(question)
        
        # حفظ السؤال والإجابة في السجل
        save_to_history(question, response, 'quran_sunnah')
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 