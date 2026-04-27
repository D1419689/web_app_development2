from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('account', __name__, url_prefix='/accounts')

@bp.route('/')
def index():
    """
    顯示所有帳戶列表。
    處理邏輯：呼叫 Account.get_all()。
    輸出：渲染 accounts/index.html。
    """
    pass

@bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    新增帳戶。
    GET: 顯示新增帳戶表單 accounts/form.html。
    POST: 接收資料並呼叫 Account.create()，成功則重導向。
    """
    pass

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯帳戶。
    GET: 取出帳戶資料並渲染 accounts/form.html。
    POST: 接收資料並呼叫 Account.update()，成功則重導向。
    """
    pass
