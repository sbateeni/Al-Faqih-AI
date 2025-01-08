from datetime import datetime
from . import db

class Fatwa(db.Model):
    """نموذج الفتوى في قاعدة البيانات"""
    
    __tablename__ = 'fatwas'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    madhahib = db.Column(db.JSON, nullable=True)  # قائمة المذاهب المختارة
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """حفظ الفتوى في قاعدة البيانات"""
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """تحويل الفتوى إلى قاموس"""
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'madhahib': self.madhahib,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
