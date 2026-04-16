from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理會員註冊請求。
    GET: 渲染註冊表單 'auth/register.html'。
    POST: 接收表單資料，檢核資料並使用 User model 寫入資料庫加密密碼。
          成功後重導向至登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理會員登入請求。
    GET: 渲染登入表單 'auth/login.html'。
    POST: 驗證帳號與密碼，正確則建立 session。
          成功後重導向至首頁。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理登出請求。
    清除 session 資料，重導向至首頁。
    """
    pass
