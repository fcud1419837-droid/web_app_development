from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, abort
)
from app.models.lot import Lot
from app.models.record import Record
from app.routes.auth import login_required

fortune_bp = Blueprint('fortune', __name__)


@fortune_bp.route('/draw', methods=['GET', 'POST'])
@login_required
def draw():
    """
    GET : 顯示求籤與擲筊介面 (fortune/draw.html)。
    POST: 後端隨機抽一支籤 → 儲存為歷史紀錄 → 導向結果頁面。
    """
    if request.method == 'POST':
        lot = Lot.get_random()

        if lot is None:
            flash('籤詩資料庫尚未建立，請聯絡管理員。', 'danger')
            return redirect(url_for('fortune.draw'))

        record_id = Record.create(user_id=g.user.id, lot_id=lot.id)
        return redirect(url_for('fortune.result', record_id=record_id))

    return render_template('fortune/draw.html')


@fortune_bp.route('/result/<int:record_id>')
def result(record_id):
    """
    顯示指定抽籤紀錄的籤詩結果與解籤說明。
    此頁面允許公開存取（方便社群分享），若紀錄不存在則回傳 404。
    """
    record = Record.get_by_id(record_id)
    if record is None:
        abort(404)

    return render_template('fortune/result.html', record=record)
