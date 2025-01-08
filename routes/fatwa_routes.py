from flask import Blueprint, request, jsonify
from models.chat import Chat, db
from utils.gemini_helper import GeminiHelper

fatwa_bp = Blueprint('fatwa', __name__)

@fatwa_bp.route('/fatwa', methods=['POST'])
def get_fatwa():
    """الحصول على فتوى من النموذج"""
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'الرجاء إدخال سؤال'}), 400

        # تهيئة Gemini API
        gemini = GeminiHelper.get_instance()
        if not gemini.is_initialized():
            return jsonify({'error': 'لم يتم تهيئة Gemini API. الرجاء إدخال مفتاح API صالح'}), 400

        # إضافة السياق للسؤال
        context = """أنت عالم إسلامي متخصص في الفقه الإسلامي. مهمتك هي:
        1. الإجابة على الأسئلة الفقهية بدقة وموضوعية
        2. الاستناد إلى القرآن والسنة والإجماع والقياس
        3. ذكر الدليل من القرآن أو السنة إن وجد
        4. ذكر آراء المذاهب الأربعة في المسألة إن وجدت خلافات
        5. التركيز على الرأي الراجح مع ذكر سبب الترجيح
        
        السؤال هو: """
        
        full_prompt = context + question

        # الحصول على الإجابة من النموذج
        response = gemini.generate_text(full_prompt)
        
        if not response:
            return jsonify({'error': 'لم نتمكن من الحصول على إجابة. حاول مرة أخرى'}), 500

        # حفظ السؤال والإجابة في قاعدة البيانات
        chat = Chat(
            question=question,
            answer=response,
            chat_type='fatwa'
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            'answer': response,
            'chat_id': chat.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
