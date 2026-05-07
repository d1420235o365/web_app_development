from flask import Blueprint, render_template, request, redirect, url_for, session

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """管理員後台概覽"""
    pass

@admin_bp.route('/book/add', methods=['GET', 'POST'])
def add_book():
    """新增書籍頁面與邏輯"""
    pass

@admin_bp.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """編輯書籍頁面與邏輯"""
    pass

@admin_bp.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """執行刪除書籍動作"""
    pass

@admin_bp.route('/overdue')
def overdue_list():
    """顯示逾期清單"""
    pass
