from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('budget', __name__, url_prefix='/budgets')

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    預算設定與列表。
    GET: 呼叫 Budget.get_all() 顯示目前所有預算設定，並渲染 budgets/index.html。
    POST: 接收新預算設定，呼叫 Budget.create() 或 Budget.update()，重導向回本頁。
    """
    pass
