import os
import sys

# إضافة المجلد الحالي إلى مسار Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from config.config import Config
from models.chat import APIKey, db
from utils.gemini_helper import GeminiHelper
from routes.chat_routes import chat_bp
from routes.page_routes import page_bp
from routes.quran_sunnah_routes import quran_sunnah_bp
from routes.history_routes import history_bp
from routes.comments_routes import comments_bp
from routes.api_key_routes import api_key_bp
from routes.fatwa_routes import fatwa_bp
from flask_caching import Cache
from inheritance_calculator import InheritanceCalculator

def create_app():
    """إنشاء وتهيئة تطبيق Flask"""
    app = Flask(__name__)
    
    # تحميل وتحقق من الإعدادات
    app.config.from_object(Config)
    Config.validate_config()
    
    # تهيئة قاعدة البيانات
    db.init_app(app)
    
    # تهيئة التخزين المؤقت
    cache = Cache(app, config={
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 300
    })
    
    with app.app_context():
        # إنشاء جداول قاعدة البيانات
        db.create_all()
        
        # تهيئة Gemini API
        active_key = None
        try:
            active_key_record = APIKey.query.filter_by(is_active=True).first()
            if active_key_record:
                active_key = active_key_record.key
            elif Config.GEMINI_API_KEY:  # استخدام المفتاح من متغيرات البيئة إذا كان متوفراً
                active_key = Config.GEMINI_API_KEY
        except Exception as e:
            print(f"خطأ في استرجاع مفتاح API: {str(e)}")
    
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
    app.register_blueprint(fatwa_bp, url_prefix='/api')

    @app.route('/inheritance')
    def inheritance():
        return render_template('inheritance.html')

    @app.route('/api/inheritance', methods=['POST'])
    def calculate_inheritance():
        try:
            data = request.get_json()
            calculator = InheritanceCalculator()
            result = calculator.calculate_shares(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return app

app = create_app()  # إنشاء نسخة من التطبيق للاستخدام مع gunicorn

if __name__ == '__main__':
    app.run(debug=True)