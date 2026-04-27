import os
from flask import Flask
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

def create_app():
    # 初始化 Flask 應用程式
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    )

    # 確保 instance 資料夾存在 (用來放 database.db)
    os.makedirs(app.instance_path, exist_ok=True)

    # 註冊路由 Blueprints
    from .routes import init_app as init_routes
    init_routes(app)

    return app
