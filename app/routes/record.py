from flask import Blueprint, render_template, request, redirect, url_for, Response

bp = Blueprint('record', __name__, url_prefix='/records')

@bp.route('/')
def index():
    """
    顯示所有收支紀錄。
    輸入：可選的 query string 篩選條件 (月份、類別等)。
    處理邏輯：呼叫 Record.get_all()。
    輸出：渲染 records/index.html。
    """
    pass

@bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    新增收支。
    GET: 取得帳戶列表並渲染 records/form.html。
    POST: 接收表單資料，驗證後呼叫 Record.create()，成功則重導向。
    """
    pass

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯特定收支。
    GET: 用 Record.get_by_id(id) 取出資料並渲染 records/form.html。
    POST: 接收表單更新，呼叫 Record.update()，成功則重導向。
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除特定收支。
    處理邏輯：呼叫 Record.delete()。
    輸出：重導向回 /records。
    """
    pass

@bp.route('/export')
def export():
    """
    匯出 CSV。
    處理邏輯：取得資料轉為 CSV 格式字串。
    輸出：回傳帶有 text/csv content-type 的 HTTP Response。
    """
    pass
