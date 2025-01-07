from datetime import datetime
from models.chat import db

class Comment(db.Model):
    """نموذج للتعليقات"""
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    is_correction = db.Column(db.Boolean, default=False)  # هل هو تصحيح أم تعليق عادي
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            'id': self.id,
            'history_id': self.history_id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'likes': self.likes,
            'is_correction': self.is_correction,
            'status': self.status
        } 