from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.account import Account

bp = Blueprint('account', __name__, url_prefix='/accounts')

@bp.route('/')
def index():
    """
    顯示所有帳戶列表。
    處理邏輯：呼叫 Account.get_all()。
    輸出：渲染 accounts/index.html。
    """
    accounts = Account.get_all()
    return render_template('accounts/index.html', accounts=accounts)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    新增帳戶。
    GET: 顯示新增帳戶表單 accounts/form.html。
    POST: 接收資料並呼叫 Account.create()，成功則重導向。
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        initial_balance = request.form.get('initial_balance', 0.0)

        if not name:
            flash('帳戶名稱為必填欄位！', 'danger')
            return render_template('accounts/form.html', account=None)

        try:
            initial_balance = float(initial_balance)
        except ValueError:
            flash('初始餘額必須為數字！', 'danger')
            return render_template('accounts/form.html', account=None)

        account_id = Account.create(name, initial_balance)
        if account_id:
            flash('帳戶新增成功！', 'success')
            return redirect(url_for('account.index'))
        else:
            flash('帳戶新增失敗，請稍後再試。', 'danger')

    return render_template('accounts/form.html', account=None)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯帳戶。
    GET: 取出帳戶資料並渲染 accounts/form.html。
    POST: 接收資料並呼叫 Account.update()，成功則重導向。
    """
    account = Account.get_by_id(id)
    if not account:
        flash('找不到該帳戶！', 'danger')
        return redirect(url_for('account.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        initial_balance = request.form.get('initial_balance', 0.0)

        if not name:
            flash('帳戶名稱為必填欄位！', 'danger')
            return render_template('accounts/form.html', account=account)

        try:
            initial_balance = float(initial_balance)
        except ValueError:
            flash('初始餘額必須為數字！', 'danger')
            return render_template('accounts/form.html', account=account)

        success = Account.update(id, name, initial_balance)
        if success:
            flash('帳戶更新成功！', 'success')
            return redirect(url_for('account.index'))
        else:
            flash('帳戶更新失敗，請稍後再試。', 'danger')

    return render_template('accounts/form.html', account=account)
