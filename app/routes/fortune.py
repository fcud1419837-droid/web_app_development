from flask import Blueprint

fortune_bp = Blueprint('fortune', __name__)

@fortune_bp.route('/draw', methods=['GET', 'POST'])
def draw():
    """
    處理求籤流程。
    GET: 渲染求籤與擲筊介面 'fortune/draw.html'。
    POST: 後端隨機抽一支籤，呼叫 Record model 把這次抽籤儲存起來。
          成功之後重導向至 /fortune/result/<record_id> 頁面。
    """
    pass

@fortune_bp.route('/result/<int:record_id>')
def result(record_id):
    """
    顯示特定紀錄的籤詩結果。
    必須檢查紀錄是否存在。可以視實作加入分享邏輯。
    渲染 'fortune/result.html'。
    """
    pass
