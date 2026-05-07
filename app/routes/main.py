from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.book import Book
from app.models.borrow_record import BorrowRecord

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """顯示首頁與書籍搜尋列表"""
    search_query = request.args.get('q', '')
    if search_query:
        # 簡單的標題模糊搜尋
        books = Book.query.filter(Book.title.contains(search_query)).all()
    else:
        books = Book.get_all()
    return render_template('index.html', books=books, query=search_query)

@main_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    """顯示特定書籍的詳細資訊"""
    book = Book.get_by_id(book_id)
    if not book:
        flash('找不到該書籍', 'warning')
        return redirect(url_for('main.index'))
    return render_template('book_detail.html', book=book)

@main_bp.route('/profile')
def profile():
    """顯示個人借閱中心"""
    if 'user_id' not in session:
        flash('請先登入以查看個人紀錄', 'info')
        return redirect(url_for('auth.login'))
    
    active_records = BorrowRecord.get_active_by_user(session['user_id'])
    # 這裡可以擴充取得歷史紀錄
    return render_template('profile.html', records=active_records)
