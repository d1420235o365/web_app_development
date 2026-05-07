from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """使用者/管理員登入頁面與邏輯"""
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """新使用者註冊頁面與邏輯"""
    pass

@auth_bp.route('/logout')
def logout():
    """執行登出並清除 Session"""
    pass
