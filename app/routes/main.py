from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁請求，判斷是否已登入來決定顯示登入狀態。
    回傳首頁模板 'index.html'。
    """
    pass

@main_bp.route('/profile/history')
def history():
    """
    顯示會員所有的抽籤與測算紀錄。
    必須檢查會員是否已經登入，未登入則導向登入頁面。
    呼叫 Record model 取得過去歷程，並渲染 'profile/history.html'。
    """
    pass
