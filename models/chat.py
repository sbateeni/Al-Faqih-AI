from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Chat(db.Model):
    """نموذج المحادثات"""
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    chat_type = db.Column(db.String(50), nullable=False)  # individual, group, fatwa, quran_sunnah
    scholar = db.Column(db.String(100), nullable=True)    # للمحادثات الفردية
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """تحويل المحادثة إلى قاموس"""
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'chat_type': self.chat_type,
            'scholar': self.scholar,
            'created_at': self.created_at.isoformat()
        } 

class APIKey(db.Model):
    """نموذج مفتاح API"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        """تحويل مفتاح API إلى قاموس"""
        return {
            'id': self.id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 