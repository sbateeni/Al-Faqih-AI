import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env إذا كان موجوداً
load_dotenv()

class Config:
    # إعدادات Flask
    FLASK_APP = "app.py"
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///chat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات Gemini API
    GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')  # تغيير اسم المتغير ليتوافق مع render.yaml
    
    # السماح بتشغيل التطبيق بدون مفتاح API في البداية
    @classmethod
    def validate_config(cls):
        """التحقق من صحة الإعدادات"""
        if not cls.GEMINI_API_KEY:
            print("تحذير: لم يتم تعيين GOOGLE_API_KEY. بعض الوظائف قد لا تعمل.") 