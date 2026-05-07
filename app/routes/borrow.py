from flask import Blueprint, request, redirect, url_for, session, flash
from app.models.book import Book
from app.models.borrow_record import BorrowRecord

borrow_bp = Blueprint('borrow', __name__)

@borrow_bp.route('/book/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    """執行借書動作"""
    if 'user_id' not in session:
        flash('請先登入後再借書', 'warning')
        return redirect(url_for('auth.login'))
    
    book = Book.get_by_id(book_id)
    if not book or book.status != 'Available':
        flash('書籍目前不可借閱', 'danger')
        return redirect(url_for('main.book_detail', book_id=book_id))
    
    # 建立借閱紀錄
    if BorrowRecord.create(user_id=session['user_id'], book_id=book_id):
        # 更新書籍狀態
        book.update(status='Borrowed')
        flash(f'成功借閱《{book.title}》！', 'success')
    else:
        flash('借閱失敗，伺服器錯誤', 'danger')
        
    return redirect(url_for('main.profile'))

@borrow_bp.route('/book/return/<int:record_id>', methods=['POST'])
def return_book(record_id):
    """執行還書動作"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    record = BorrowRecord.get_by_id(record_id)
    if not record or record.user_id != session['user_id'] or record.status != 'Active':
        flash('無效的歸還請求', 'danger')
        return redirect(url_for('main.profile'))
    
    # 更新紀錄
    if record.mark_as_returned():
        # 更新書籍狀態
        book = Book.get_by_id(record.book_id)
        if book:
            book.update(status='Available')
        flash('書籍已成功歸還', 'success')
    else:
        flash('歸還失敗', 'danger')
        
    return redirect(url_for('main.profile'))
