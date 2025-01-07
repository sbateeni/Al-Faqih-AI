import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

class Config:
    # إعدادات Flask
    FLASK_APP = "app.py"
    FLASK_ENV = "development"
    DEBUG = True
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("الرجاء تعيين GEMINI_API_KEY في ملف .env") 