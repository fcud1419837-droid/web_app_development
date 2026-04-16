from flask import Blueprint, render_template, request, flash, redirect, url_for

donate_bp = Blueprint('donate', __name__)


@donate_bp.route('/')
def index():
    """
    顯示香油錢捐款頁面，內含捐款方案說明與匯款資訊 (donate/index.html)。
    """
    return render_template('donate/index.html')


@donate_bp.route('/success', methods=['GET', 'POST'])
def success():
    """
    GET : 直接瀏覽感謝頁面。
    POST: 接收捐款표單（或第三方金流回傳），顯示捐款成功感謝畫面 (donate/success.html)。
    """
    amount = None
    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        if not amount:
            flash('請填寫捐款金額。', 'danger')
            return redirect(url_for('donate.index'))
        flash(f'感謝您捐獻 NT${amount} 香油錢，神明保佑！', 'success')

    return render_template('donate/success.html', amount=amount)
