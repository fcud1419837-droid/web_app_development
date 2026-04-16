from flask import Blueprint

donate_bp = Blueprint('donate', __name__)

@donate_bp.route('/')
def index():
    """
    處理香油錢頁面的進入請求。
    渲染香油錢付款表單或是轉帳資訊 'donate/index.html'。
    """
    pass

@donate_bp.route('/success', methods=['GET', 'POST'])
def success():
    """
    捐獻成功頁面 / 金流回傳頁面。
    GET: 渲染感謝畫面 'donate/success.html'。
    POST: （可選）接收第三方綠界或其他金流 API 呼叫，驗證訂單後顯示感謝畫面。
    """
    pass
