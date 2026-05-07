from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from functools import wraps
from app.models.book import Book
from app.models.borrow_record import BorrowRecord

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('此操作需要管理員權限', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理員後台概覽"""
    total_books = len(Book.get_all())
    active_borrows = len(BorrowRecord.query.filter_by(status='Active').all())
    return render_template('admin/dashboard.html', total_books=total_books, active_borrows=active_borrows)

@admin_bp.route('/book/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    """新增書籍頁面與邏輯"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        category = request.form.get('category')

        if not title:
            flash('書名為必填欄位', 'danger')
            return render_template('admin/book_form.html', action='Add')

        if Book.create(title=title, author=author, isbn=isbn, category=category):
            flash('成功新增書籍', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('新增失敗', 'danger')

    return render_template('admin/book_form.html', action='Add')

@admin_bp.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    """編輯書籍頁面與邏輯"""
    book = Book.get_by_id(book_id)
    if not book:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        category = request.form.get('category')

        if book.update(title=title, author=author, isbn=isbn, category=category):
            flash('更新成功', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('更新失敗', 'danger')

    return render_template('admin/book_form.html', action='Edit', book=book)

@admin_bp.route('/book/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    """執行刪除書籍動作"""
    book = Book.get_by_id(book_id)
    if book and book.delete():
        flash('書籍已刪除', 'success')
    else:
        flash('刪除失敗', 'danger')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/overdue')
@admin_required
def overdue_list():
    """顯示逾期清單"""
    # 簡單模擬：超過 14 天即為逾期
    # 這裡僅顯示所有借閱中紀錄作為示範
    overdue_records = BorrowRecord.query.filter_by(status='Active').all()
    return render_template('admin/overdue.html', records=overdue_records)
