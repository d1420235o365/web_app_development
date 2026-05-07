from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """使用者/管理員登入頁面與邏輯"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫帳號與密碼', 'danger')
            return render_template('login.html')

        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'歡迎回來, {user.username}！', 'success')
            
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        
        flash('帳號或密碼錯誤', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """新使用者註冊頁面與邏輯"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password:
            flash('請填寫所有必填欄位', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('密碼不一致', 'danger')
            return render_template('register.html')

        if User.get_by_username(username):
            flash('此帳號已存在', 'warning')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)
        # 預設註冊為借閱者 (borrower)
        if User.create(username=username, password_hash=hashed_pw):
            flash('註冊成功，請登入', 'success')
            return redirect(url_for('auth.login'))
        
        flash('註冊失敗，請稍後再試', 'danger')

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """執行登出並清除 Session"""
    session.clear()
    flash('您已成功登出', 'info')
    return redirect(url_for('main.index'))
