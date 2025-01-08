from flask import Blueprint, request, jsonify, render_template
from models.fatwa import Fatwa, db
from utils.gemini_helper import GeminiHelper
from datetime import datetime

fatwa_bp = Blueprint('fatwa', __name__)

@fatwa_bp.route('/fatwa')
def fatwa_page():
    """صفحة الفتوى"""
    return render_template('fatwa.html')

@fatwa_bp.route('/api/fatwa', methods=['POST'])
def get_fatwa():
    try:
        data = request.get_json()
        question = data.get('question')
        madhahib = data.get('madhahib', ['hanafi', 'maliki', 'shafii', 'hanbali'])
        
        if not question:
            return jsonify({'error': 'الرجاء إدخال السؤال'}), 400

        # تهيئة Gemini API
        gemini = GeminiHelper.get_instance()
        if not gemini.is_initialized():
            return jsonify({'error': 'لم يتم تهيئة Gemini API. الرجاء إدخال مفتاح API صالح'}), 400

        # تحضير السياق للفتوى
        context = f"""أنت فقيه متخصص في الفقه الإسلامي. مهمتك هي الإجابة على الأسئلة الشرعية.
        يجب أن تقدم الفتوى بالتفصيل مع ذكر الأدلة من القرآن والسنة.
        
        المطلوب ذكر آراء المذاهب التالية: {', '.join(madhahib)}
        
        قم بتنظيم الإجابة في الأقسام التالية:
        1. الحكم الشرعي
        2. الأدلة من القرآن والسنة
        3. آراء المذاهب المختلفة
        4. الخلاصة والترجيح
        5. التوصيات العملية

        السؤال: {question}"""

        # الحصول على الفتوى من Gemini
        response = gemini.generate_text(context)

        if not response:
            return jsonify({'error': 'لم نتمكن من الحصول على إجابة. حاول مرة أخرى'}), 500

        # حفظ الفتوى في قاعدة البيانات
        fatwa = Fatwa(
            question=question,
            answer=response,
            madhahib=madhahib,
            timestamp=datetime.utcnow()
        )
        db.session.add(fatwa)
        db.session.commit()

        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fatwa_bp.route('/api/fatwa/recent', methods=['GET'])
def get_recent_fatwas():
    try:
        # الحصول على آخر 10 فتاوى
        fatwas = Fatwa.query.order_by(Fatwa.timestamp.desc()).limit(10).all()
        
        recent_fatwas = []
        for fatwa in fatwas:
            recent_fatwas.append(fatwa.to_dict())
        
        return jsonify(recent_fatwas)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
