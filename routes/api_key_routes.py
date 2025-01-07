from flask import Blueprint, request, jsonify
from models.chat import db, APIKey
from utils.gemini_helper import GeminiHelper

api_key_bp = Blueprint('api_key', __name__)

@api_key_bp.route('/api-key', methods=['POST'])
def set_api_key():
    """تعيين مفتاح API جديد"""
    data = request.get_json()
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'مفتاح API مطلوب'}), 400
        
    # تعطيل جميع المفاتيح السابقة
    APIKey.query.update({APIKey.is_active: False})
    
    # إنشاء مفتاح جديد
    new_key = APIKey(key=api_key, is_active=True)
    db.session.add(new_key)
    
    try:
        db.session.commit()
        # تحديث مفتاح API في GeminiHelper
        gemini = GeminiHelper.get_instance()
        if gemini.setup_api(api_key):
            return jsonify({'message': 'تم حفظ مفتاح API بنجاح'}), 200
        else:
            return jsonify({'error': 'مفتاح API غير صالح'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_key_bp.route('/api-key/status', methods=['GET'])
def get_api_key_status():
    """التحقق من حالة مفتاح API"""
    active_key = APIKey.query.filter_by(is_active=True).first()
    return jsonify({
        'has_active_key': active_key is not None,
        'last_updated': active_key.updated_at.isoformat() if active_key else None
    }) 