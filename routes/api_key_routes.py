from flask import Blueprint, request, jsonify
from models.api_keys import APIKeyManager
from functools import wraps
import jwt
from datetime import datetime, timedelta
from config.config import Config

api_key_bp = Blueprint('api_key', __name__)

def token_required(f):
    """مصادقة التوكن للمستخدم"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@api_key_bp.route('/api-key', methods=['POST'])
@token_required
def save_api_key(current_user):
    """حفظ مفتاح API للمستخدم"""
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
            
        success = APIKeyManager.save_api_key(current_user, api_key)
        if success:
            return jsonify({
                'message': 'API key saved successfully',
                'user_id': current_user
            })
        return jsonify({'error': 'Failed to save API key'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_key_bp.route('/api-key/verify', methods=['POST'])
@token_required
def verify_api_key(current_user):
    """التحقق من صحة مفتاح API"""
    try:
        data = request.get_json()
        provided_key = data.get('api_key')
        
        if not provided_key:
            return jsonify({'error': 'API key is required'}), 400
            
        is_valid = APIKeyManager.get_api_key(current_user, provided_key)
        return jsonify({'valid': is_valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_key_bp.route('/api-key', methods=['DELETE'])
@token_required
def deactivate_api_key(current_user):
    """إلغاء تفعيل مفتاح API"""
    try:
        success = APIKeyManager.deactivate_api_key(current_user)
        if success:
            return jsonify({'message': 'API key deactivated successfully'})
        return jsonify({'error': 'Failed to deactivate API key'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500