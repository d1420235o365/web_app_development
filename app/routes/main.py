from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """顯示首頁與書籍搜尋列表"""
    pass

@main_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    """顯示特定書籍的詳細資訊"""
    pass

@main_bp.route('/profile')
def profile():
    """顯示個人借閱中心"""
    pass
