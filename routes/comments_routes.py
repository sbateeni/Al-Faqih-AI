from flask import Blueprint, jsonify, request
from models.comments import Comment, db
from models.history import History

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/history/<int:history_id>/comments', methods=['GET'])
def get_comments(history_id):
    """الحصول على تعليقات عنصر معين"""
    try:
        comments = Comment.query.filter_by(
            history_id=history_id,
            status='approved'
        ).order_by(Comment.created_at.desc()).all()
        
        return jsonify([comment.to_dict() for comment in comments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comments_bp.route('/history/<int:history_id>/comments', methods=['POST'])
def add_comment(history_id):
    """إضافة تعليق جديد"""
    try:
        # التحقق من وجود العنصر
        history_item = History.query.get_or_404(history_id)
        
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'الرجاء إدخال نص التعليق'}), 400
            
        comment = Comment(
            history_id=history_id,
            text=data['text'],
            is_correction=data.get('is_correction', False)
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify(comment.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comments_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """الإعجاب بتعليق"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        comment.likes += 1
        db.session.commit()
        return jsonify(comment.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comments_bp.route('/comments/<int:comment_id>/status', methods=['PUT'])
def update_comment_status(comment_id):
    """تحديث حالة التعليق (للمشرفين)"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        data = request.json
        if not data or 'status' not in data:
            return jsonify({'error': 'الرجاء تحديد الحالة'}), 400
            
        status = data['status']
        if status not in ['pending', 'approved', 'rejected']:
            return jsonify({'error': 'حالة غير صالحة'}), 400
            
        comment.status = status
        db.session.commit()
        
        return jsonify(comment.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500 