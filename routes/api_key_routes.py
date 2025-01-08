from flask import Blueprint, request, jsonify
from models.api_keys import APIKeyManager
from models.chat import APIKey, db
from utils.gemini_helper import GeminiHelper
from config.config import Config

api_key_bp = Blueprint('api_key', __name__)

@api_key_bp.route('/api-key', methods=['POST'])
def set_api_key():
    """تعيين مفتاح API جديد"""
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'مفتاح API مطلوب'}), 400
        
        if len(api_key.strip()) < 10:  # التحقق من طول المفتاح
            return jsonify({'error': 'مفتاح API غير صالح. يجب أن يكون طوله أكبر من 10 أحرف'}), 400
            
        # تهيئة GeminiHelper للتحقق من صحة المفتاح
        gemini = GeminiHelper.get_instance()
        if not gemini.setup_api(api_key):
            return jsonify({
                'error': 'مفتاح API غير صالح',
                'details': gemini.get_last_error()
            }), 400
            
        # تعطيل جميع المفاتيح السابقة
        APIKey.query.update({APIKey.is_active: False})
        
        # إنشاء مفتاح جديد
        new_key = APIKey(key=api_key, is_active=True)
        db.session.add(new_key)
        
        try:
            db.session.commit()
            Config.GEMINI_API_KEY = api_key
            return jsonify({
                'message': 'تم حفظ مفتاح API بنجاح',
                'status': 'success'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'حدث خطأ أثناء حفظ المفتاح',
                'details': str(e)
            }), 500
    except Exception as e:
        return jsonify({
            'error': 'حدث خطأ غير متوقع',
            'details': str(e)
        }), 500

@api_key_bp.route('/api-key/status', methods=['GET'])
def get_api_key_status():
    """التحقق من حالة مفتاح API"""
    try:
        active_key = APIKey.query.filter_by(is_active=True).first()
        gemini = GeminiHelper.get_instance()
        
        status = {
            'has_active_key': active_key is not None,
            'last_updated': active_key.updated_at.isoformat() if active_key else None,
            'is_working': False,
            'error': None
        }
        
        if active_key:
            # التحقق من صحة المفتاح
            if gemini.check_connection():
                status['is_working'] = True
            else:
                status['error'] = gemini.get_last_error()
        
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'error': 'حدث خطأ أثناء التحقق من حالة المفتاح',
            'details': str(e)
        }), 500

@api_key_bp.route('/api-key', methods=['DELETE'])
def delete_api_key():
    """حذف مفتاح API الحالي"""
    try:
        # حذف جميع المفاتيح
        APIKey.query.delete()
        db.session.commit()
        
        # إعادة تهيئة GeminiHelper
        gemini = GeminiHelper.get_instance()
        gemini._is_initialized = False
        gemini.model = None
        Config.GEMINI_API_KEY = None
        
        return jsonify({
            'message': 'تم حذف مفتاح API بنجاح',
            'status': 'success'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'حدث خطأ أثناء حذف المفتاح',
            'details': str(e)
        }), 500