import os
import sqlite3
from flask import Flask, g
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # 基本設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化資料庫連線管理
    from app.models import close_db
    app.teardown_appcontext(close_db)

    # 建立 CLI 指令：flask init-db
    @app.cli.command('init-db')
    def init_db_command():
        """初始化資料庫，建立所有資料表。"""
        from app.models import init_db
        init_db()
        print('資料庫已初始化。')

    # 註冊 Blueprints
    from app.routes import init_app as init_routes
    init_routes(app)

    return app
