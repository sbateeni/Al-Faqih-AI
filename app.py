import os
import sys

# إضافة المجلد الحالي إلى مسار Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config.config import Config
from models.chat import APIKey, db
from utils.gemini_helper import GeminiHelper
from routes.chat_routes import chat_bp
from routes.page_routes import page_bp
from routes.quran_sunnah_routes import quran_sunnah_bp
from routes.history_routes import history_bp
from routes.comments_routes import comments_bp
from routes.api_key_routes import api_key_bp
from flask_caching import Cache

def create_app():
    """إنشاء وتهيئة تطبيق Flask"""
    app = Flask(__name__)
    
    # تحميل الإعدادات
    app.config.from_object(Config)
    
    # تهيئة التخزين المؤقت
    cache = Cache(app, config={
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 300
    })
    
    # تهيئة قاعدة البيانات
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # تهيئة Gemini API
    active_key = None
    with app.app_context():
        active_key_record = APIKey.query.filter_by(is_active=True).first()
        if active_key_record:
            active_key = active_key_record.key
    
    gemini = GeminiHelper.get_instance()
    if active_key and not gemini.setup_api(active_key):
        print("تحذير: فشل الاتصال بـ Gemini API")
    
    # تسجيل Blueprints
    app.register_blueprint(page_bp)
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(quran_sunnah_bp)
    app.register_blueprint(history_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(api_key_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 