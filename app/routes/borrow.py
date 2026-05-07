from flask import Blueprint, request, redirect, url_for, session

borrow_bp = Blueprint('borrow', __name__)

@borrow_bp.route('/book/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    """執行借書動作"""
    pass

@borrow_bp.route('/book/return/<int:record_id>', methods=['POST'])
def return_book(record_id):
    """執行還書動作"""
    pass
