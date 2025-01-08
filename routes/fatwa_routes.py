from flask import Blueprint, request, jsonify, render_template
from models.chat import Chat, db
from models.fatwa import Fatwa
from utils.gemini_helper import GeminiHelper
from utils.gemini import get_gemini_response
from datetime import datetime

fatwa_bp = Blueprint('fatwa', __name__)

@fatwa_bp.route('/fatwa')
def fatwa_page():
    """عرض صفحة الفتوى"""
    return render_template('fatwa.html')

@fatwa_bp.route('/api/fatwa', methods=['POST'])
def get_fatwa():
    try:
        data = request.get_json()
        question = data.get('question')
        madhahib = data.get('madhahib', ['hanafi', 'maliki', 'shafii', 'hanbali'])
        
        if not question:
            return jsonify({'error': 'الرجاء إدخال السؤال'}), 400

        # تحضير السياق للفتوى
        context = f"""أنت فقيه متخصص في الفقه الإسلامي. مهمتك هي الإجابة على الأسئلة الشرعية.
        يجب أن تقدم الفتوى بالتفصيل مع ذكر الأدلة من القرآن والسنة.
        
        المطلوب ذكر آراء المذاهب التالية: {', '.join(madhahib)}
        
        قم بتنظيم الإجابة في الأقسام التالية:
        1. الحكم الشرعي
        2. الأدلة من القرآن والسنة
        3. آراء المذاهب المختلفة
        4. الخلاصة والترجيح
        5. التوصيات العملية"""

        # الحصول على الفتوى من Gemini
        response = get_gemini_response(context + "\n\nالسؤال: " + question)

        # حفظ الفتوى في قاعدة البيانات
        fatwa = Fatwa(
            question=question,
            answer=response,
            madhahib=madhahib,
            timestamp=datetime.utcnow()
        )
        fatwa.save()

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
            recent_fatwas.append({
                'question': fatwa.question,
                'answer': fatwa.answer,
                'madhahib': fatwa.madhahib,
                'timestamp': fatwa.timestamp.isoformat()
            })
        
        return jsonify(recent_fatwas)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_fatwa(response):
    """تنسيق الفتوى لعرضها بشكل منظم"""
    sections = []
    current_section = {'title': '', 'content': []}
    
    for line in response.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # التعرف على العناوين الرئيسية
        if line.startswith(('الحكم:', 'الدليل:', 'المذاهب:', 'الخلاصة:', 'التوصيات:')):
            if current_section['content']:
                sections.append(current_section)
            current_section = {'title': line, 'content': []}
            continue
            
        # إضافة المحتوى
        current_section['content'].append(line)
    
    if current_section['content']:
        sections.append(current_section)
    
    # تنسيق النتائج النهائية
    formatted_sections = []
    for section in sections:
        formatted_content = []
        current_point = []
        
        for line in section['content']:
            if line.startswith(('-', '•', '*')) or line[0].isdigit():
                if current_point:
                    formatted_content.append(' '.join(current_point))
                current_point = [line]
            else:
                current_point.append(line)
                
        if current_point:
            formatted_content.append(' '.join(current_point))
            
        formatted_sections.append({
            'title': section['title'],
            'content': '<br>'.join(formatted_content)
        })
    
    return formatted_sections
