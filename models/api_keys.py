from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class UserAPIKey(db.Model):
    """نموذج لتخزين مفاتيح API للمستخدمين"""
    
    __tablename__ = 'user_api_keys'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)  # معرف المستخدم (يمكن أن يكون البريد الإلكتروني أو رقم الهاتف)
    api_key_hash = db.Column(db.String(500), nullable=False)  # تخزين مشفر للمفتاح
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_used = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_api_key(self, api_key: str):
        """تشفير وتخزين مفتاح API"""
        self.api_key_hash = generate_password_hash(api_key)
    
    def check_api_key(self, api_key: str) -> bool:
        """التحقق من صحة مفتاح API"""
        return check_password_hash(self.api_key_hash, api_key)
    
    def update_last_used(self):
        """تحديث وقت آخر استخدام"""
        self.last_used = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """تحويل السجل إلى قاموس"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'is_active': self.is_active
        }

class APIKeyManager:
    """مدير مفاتيح API"""
    
    @staticmethod
    def save_api_key(user_id: str, api_key: str) -> bool:
        """حفظ أو تحديث مفتاح API للمستخدم"""
        try:
            user_key = UserAPIKey.query.filter_by(user_id=user_id).first()
            if user_key:
                user_key.set_api_key(api_key)
            else:
                user_key = UserAPIKey(user_id=user_id)
                user_key.set_api_key(api_key)
                db.session.add(user_key)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving API key: {str(e)}")
            return False
    
    @staticmethod
    def get_api_key(user_id: str, provided_key: str) -> bool:
        """التحقق من صحة مفتاح API للمستخدم"""
        user_key = UserAPIKey.query.filter_by(user_id=user_id, is_active=True).first()
        if user_key and user_key.check_api_key(provided_key):
            user_key.update_last_used()
            return True
        return False
    
    @staticmethod
    def deactivate_api_key(user_id: str) -> bool:
        """إلغاء تفعيل مفتاح API للمستخدم"""
        try:
            user_key = UserAPIKey.query.filter_by(user_id=user_id).first()
            if user_key:
                user_key.is_active = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deactivating API key: {str(e)}")
            return False
