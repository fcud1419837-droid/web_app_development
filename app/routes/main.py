from flask import Blueprint, render_template, g
from app.models.record import Record
from app.routes.auth import login_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁：顯示系統介紹與功能入口。
    已登入時顯示歡迎訊息，未登入顯示引導連結。
    """
    return render_template('index.html')


@main_bp.route('/profile/history')
@login_required
def history():
    """
    會員歷史紀錄頁：列出目前登入使用者的所有抽籤紀錄。
    需要登入（由 login_required 裝飾器把關）。
    """
    records = Record.get_by_user_id(g.user.id)
    return render_template('profile/history.html', records=records)
