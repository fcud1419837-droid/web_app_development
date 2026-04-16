import functools
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


def login_required(view):
    """裝飾器：確保訪問此路由的使用者已登入，否則導向登入頁。"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('請先登入才能使用此功能。', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    """在每次請求前，從 session 載入目前登入的使用者到 g.user。"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_by_id(user_id)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET : 顯示註冊表單 (auth/register.html)。
    POST: 驗證輸入 → 建立帳號 → 導向登入頁。
    """
    if g.user:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        error = None
        if not username:
            error = '帳號不能為空。'
        elif not password:
            error = '密碼不能為空。'
        elif len(password) < 6:
            error = '密碼長度至少需要 6 個字元。'
        elif password != confirm:
            error = '兩次輸入的密碼不一致。'
        elif User.get_by_username(username) is not None:
            error = f'帳號「{username}」已被使用，請選擇其他帳號。'

        if error is None:
            User.create(username, password)
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))

        flash(error, 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET : 顯示登入表單 (auth/login.html)。
    POST: 驗證帳號密碼 → 寫入 session → 導向首頁。
    """
    if g.user:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        error = None
        user = User.get_by_username(username)

        if user is None:
            error = '帳號不存在。'
        elif not user.check_password(password):
            error = '密碼錯誤。'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash(f'歡迎回來，{user.username}！', 'success')
            return redirect(url_for('main.index'))

        flash(error, 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """清除 session 並導向首頁。"""
    session.clear()
    flash('已成功登出。', 'info')
    return redirect(url_for('main.index'))
