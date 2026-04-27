from flask import Blueprint, render_template

bp = Blueprint('index', __name__)

@bp.route('/')
def dashboard():
    """
    首頁與儀表板。
    處理邏輯：
    1. 取得當月總收入、總支出。
    2. 取得預算達成進度。
    3. 取得近期幾筆收支紀錄。
    輸出：渲染 index.html，傳遞數據供前端圖表繪製。
    """
    pass
