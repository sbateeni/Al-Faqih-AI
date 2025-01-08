from flask import Blueprint, jsonify
from models.chat import Chat, db

history_bp = Blueprint('history', __name__)

def save_to_history(question, answer, chat_type, scholar=None):
    """حفظ المحادثة في السجل"""
    try:
        chat = Chat(
            question=question,
            answer=answer,
            chat_type=chat_type,
            scholar=scholar
        )
        db.session.add(chat)
        db.session.commit()
        return chat
    except Exception as e:
        db.session.rollback()
        raise e

@history_bp.route('/history', methods=['GET'])
def get_history():
    """الحصول على سجل المحادثات"""
    try:
        chats = Chat.query.order_by(Chat.created_at.desc()).all()
        return jsonify([chat.to_dict() for chat in chats])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/history/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    """الحصول على محادثة محددة"""
    try:
        chat = Chat.query.get_or_404(chat_id)
        return jsonify(chat.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500 