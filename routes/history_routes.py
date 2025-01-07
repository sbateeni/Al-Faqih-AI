from flask import Blueprint, jsonify, request, send_file
from models.history import History, db
from utils.pdf_helper import PDFHelper
import uuid

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def get_history():
    """الحصول على سجل الأسئلة والإجابات"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        type_ = request.args.get('type')
        
        query = History.query
        
        if category:
            query = query.filter_by(category=category)
        if type_:
            query = query.filter_by(type=type_)
            
        history = query.order_by(History.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'items': [item.to_dict() for item in history.items],
            'total': history.total,
            'pages': history.pages,
            'current_page': history.page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/favorites', methods=['GET'])
def get_favorites():
    """الحصول على المفضلة"""
    try:
        favorites = History.query.filter_by(is_favorite=True).order_by(History.created_at.desc()).all()
        return jsonify([item.to_dict() for item in favorites])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/history/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """تبديل حالة المفضلة"""
    try:
        item = History.query.get_or_404(id)
        item.is_favorite = not item.is_favorite
        db.session.commit()
        return jsonify(item.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/history/<int:id>', methods=['DELETE'])
def delete_history(id):
    """حذف عنصر من السجل"""
    try:
        item = History.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'تم الحذف بنجاح'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/history/<string:share_id>', methods=['GET'])
def get_shared_item(share_id):
    """الحصول على عنصر مشترك"""
    try:
        item = History.query.filter_by(share_id=share_id).first_or_404()
        item.views += 1
        db.session.commit()
        return jsonify(item.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_to_history(question, answer, type_, category=None):
    """حفظ سؤال وإجابة في السجل"""
    try:
        history_item = History(
            question=question,
            answer=answer,
            type=type_,
            category=category,
            share_id=str(uuid.uuid4())[:8]
        )
        db.session.add(history_item)
        db.session.commit()
        return history_item
    except Exception as e:
        print(f"خطأ في حفظ السجل: {str(e)}")
        db.session.rollback()
        return None 

@history_bp.route('/history/<int:id>/export', methods=['GET'])
def export_to_pdf(id):
    """تصدير عنصر من السجل إلى PDF"""
    try:
        item = History.query.get_or_404(id)
        
        # تحضير المحتوى
        content = f"""
        <h2>السؤال:</h2>
        <p>{item.question}</p>
        
        <h2>الإجابة:</h2>
        <div>{item.answer}</div>
        
        <div class="references">
            النوع: {item.type}<br>
            التصنيف: {item.category or 'غير مصنف'}<br>
            التاريخ: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """
        
        # توليد PDF
        pdf_path = PDFHelper.generate_pdf(content, f"نتائج البحث - {item.type}")
        if not pdf_path:
            return jsonify({'error': 'فشل في توليد PDF'}), 500
            
        try:
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"result_{item.id}.pdf",
                mimetype='application/pdf'
            )
        finally:
            # حذف الملف المؤقت بعد إرساله
            PDFHelper.cleanup_temp_file(pdf_path)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500 