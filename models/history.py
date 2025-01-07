from datetime import datetime
from models.chat import db

class History(db.Model):
    """نموذج لتخزين سجل الأسئلة والإجابات"""
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # نوع السؤال (فتوى، تفسير، حديث، إلخ)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))  # تصنيف (عبادات، معاملات، عقيدة، إلخ)
    views = db.Column(db.Integer, default=0)
    share_id = db.Column(db.String(50), unique=True)  # معرف للمشاركة

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'type': self.type,
            'created_at': self.created_at.isoformat(),
            'is_favorite': self.is_favorite,
            'category': self.category,
            'views': self.views,
            'share_id': self.share_id
        } 