from flask import Blueprint, request, jsonify, render_template
from models.chat import Chat, db
from utils.gemini_helper import GeminiHelper
from datetime import datetime

fatwa_bp = Blueprint('fatwa', __name__)

@fatwa_bp.route('/fatwa')
def fatwa_page():
    """عرض صفحة الفتوى"""
    return render_template('fatwa.html')

@fatwa_bp.route('/api/fatwa', methods=['POST'])
def get_fatwa():
    """الحصول على فتوى من النموذج"""
    try:
        data = request.get_json()
        question = data.get('question')
        madhab = data.get('madhab', 'all')
        
        if not question:
            return jsonify({'error': 'الرجاء إدخال سؤال'}), 400

        # تهيئة Gemini API
        gemini = GeminiHelper.get_instance()
        if not gemini.is_initialized():
            return jsonify({'error': 'لم يتم تهيئة Gemini API. الرجاء إدخال مفتاح API صالح'}), 400

        # إضافة السياق للسؤال
        context = f"""أنت عالم إسلامي متخصص في الفقه الإسلامي. مهمتك هي:

1. تقديم الفتوى:
   - الإجابة على السؤال بوضوح ودقة
   - تقسيم الإجابة إلى نقاط مرتبة
   - استخدام لغة سهلة ومفهومة

2. الأدلة الشرعية:
   - ذكر الدليل من القرآن الكريم (مع رقم السورة والآية)
   - ذكر الدليل من السنة النبوية (مع درجة صحة الحديث)
   - ذكر الإجماع إن وجد

3. آراء المذاهب:
   {'- ذكر آراء المذاهب الأربعة في المسألة' if madhab == 'all' else f'- التركيز على رأي المذهب {madhab}'}
   - بيان سبب الاختلاف إن وجد
   - ذكر الرأي الراجح مع دليله

4. الخلاصة والتوصيات:
   - تلخيص الحكم الشرعي
   - ذكر النصائح والتوجيهات المتعلقة
   - الإشارة إلى المراجع الفقهية المعتمدة

السؤال هو: {question}
"""
        
        # الحصول على الإجابة من النموذج
        response = gemini.generate_text(context)
        
        if not response:
            return jsonify({'error': 'لم نتمكن من الحصول على إجابة. حاول مرة أخرى'}), 500

        # تنسيق الإجابة
        formatted_response = format_fatwa(response)

        # حفظ الفتوى في قاعدة البيانات
        chat = Chat(
            question=question,
            answer=response,
            chat_type='fatwa'
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            'answer': formatted_response,
            'chat_id': chat.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fatwa_bp.route('/api/fatwa/recent', methods=['GET'])
def get_recent_fatwas():
    """الحصول على آخر الفتاوى"""
    try:
        recent_fatwas = Chat.query.filter_by(chat_type='fatwa')\
            .order_by(Chat.created_at.desc())\
            .limit(5)\
            .all()
        
        return jsonify({
            'fatwas': [{
                'id': fatwa.id,
                'question': fatwa.question,
                'created_at': fatwa.created_at.isoformat()
            } for fatwa in recent_fatwas]
        })

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
