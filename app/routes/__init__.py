from flask import Flask

def init_app(app: Flask):
    from . import index, record, account, budget
    
    app.register_blueprint(index.bp)
    app.register_blueprint(record.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(budget.bp)
