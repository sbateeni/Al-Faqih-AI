from flask import Blueprint, request, jsonify, render_template
from models.chat import Chat, db
from utils.gemini_helper import GeminiHelper

quran_sunnah_bp = Blueprint('quran_sunnah', __name__)

@quran_sunnah_bp.route('/quran_sunnah')
def quran_sunnah_page():
    """عرض صفحة البحث في القرآن والسنة"""
    return render_template('quran_sunnah.html')

@quran_sunnah_bp.route('/api/quran_sunnah/search', methods=['POST'])
def search():
    """البحث في القرآن والسنة"""
    try:
        data = request.get_json()
        query = data.get('query')
        types = data.get('types', {})
        options = data.get('options', {})
        
        if not query:
            return jsonify({'error': 'الرجاء إدخال نص للبحث'}), 400

        # تهيئة Gemini API
        gemini = GeminiHelper.get_instance()
        if not gemini.is_initialized():
            return jsonify({'error': 'لم يتم تهيئة Gemini API. الرجاء إدخال مفتاح API صالح'}), 400

        # إعداد السياق بناءً على نوع البحث
        context = "أنت باحث متخصص في علوم القرآن والسنة. مهمتك هي:\n\n"
        
        if types.get('quran'):
            context += """1. البحث في القرآن الكريم:
            - ذكر الآيات المتعلقة بالموضوع
            - تقديم معلومات عن السور والآيات (رقم السورة، رقم الآية)
            - إضافة التفسير المختصر للآيات\n\n"""

        if types.get('hadith'):
            context += """2. البحث في السنة النبوية:
            - ذكر الأحاديث المتعلقة بالموضوع
            - تحديد مصدر كل حديث ودرجة صحته
            - شرح معاني الأحاديث باختصار\n\n"""

        if types.get('tafsir'):
            context += """3. التفسير والشرح:
            - تقديم تفسير العلماء للآيات
            - ذكر أقوال المفسرين المعتمدين
            - توضيح المعاني والدلالات\n\n"""

        # إضافة الخيارات المتقدمة
        if options:
            context += "مع مراعاة الخيارات التالية:\n"
            if options.get('quranSource') != 'all':
                context += f"- الاعتماد على رواية {options['quranSource']} للقرآن\n"
            if options.get('hadithSource') != 'all':
                context += f"- الاعتماد على {options['hadithSource']} للحديث\n"
            if options.get('tafsirSource') != 'all':
                context += f"- الاعتماد على {options['tafsirSource']} للتفسير\n"
            if options.get('language') != 'ar':
                context += f"- تقديم الترجمة باللغة {options['language']}\n"

        context += f"\nالسؤال أو موضوع البحث هو: {query}"

        # الحصول على الإجابة من النموذج
        response = gemini.generate_text(context)
        
        if not response:
            return jsonify({'error': 'لم نتمكن من الحصول على نتائج. حاول مرة أخرى'}), 500

        # تنسيق الإجابة
        formatted_response = format_response(response)

        # حفظ البحث في قاعدة البيانات
        chat = Chat(
            question=query,
            answer=response,
            chat_type='quran_sunnah'
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            'results': formatted_response,
            'chat_id': chat.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quran_sunnah_bp.route('/api/quran_sunnah/recent', methods=['GET'])
def get_recent_searches():
    """الحصول على آخر عمليات البحث"""
    try:
        recent_searches = Chat.query.filter_by(chat_type='quran_sunnah')\
            .order_by(Chat.created_at.desc())\
            .limit(5)\
            .all()
        
        return jsonify({
            'searches': [{
                'id': search.id,
                'query': search.question,
                'created_at': search.created_at.isoformat()
            } for search in recent_searches]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_response(response):
    """تنسيق الإجابة لعرضها بشكل منظم"""
    sections = []
    current_section = {'type': '', 'content': [], 'reference': ''}
    
    for line in response.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # التعرف على نوع القسم
        if 'القرآن' in line.lower() and not current_section['content']:
            if current_section['content']:
                sections.append(current_section)
            current_section = {'type': 'quran', 'content': [], 'reference': ''}
            continue
        elif 'حديث' in line.lower() and not current_section['content']:
            if current_section['content']:
                sections.append(current_section)
            current_section = {'type': 'hadith', 'content': [], 'reference': ''}
            continue
        elif 'تفسير' in line.lower() and not current_section['content']:
            if current_section['content']:
                sections.append(current_section)
            current_section = {'type': 'tafsir', 'content': [], 'reference': ''}
            continue
            
        # التعرف على المراجع
        if '[' in line and ']' in line:
            current_section['reference'] = line
        else:
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
            'type': section['type'],
            'content': '<br>'.join(formatted_content),
            'reference': section['reference']
        })
    
    return formatted_sections