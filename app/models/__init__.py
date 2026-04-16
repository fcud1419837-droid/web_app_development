import sqlite3
import os
from flask import g, current_app


def get_db():
    """
    獲取資料庫連線。
    如果當前 app context 中沒有連線，就建立一個新的並存入 g。
    """
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """關閉資料庫連線（在 app context 結束時自動呼叫）。"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """根據 database/schema.sql 建立所有資料表。"""
    db = get_db()
    # 取得專案根目錄（app/__init__.py 的上層）
    project_root = os.path.join(current_app.root_path, '..')
    schema_path = os.path.join(project_root, 'database', 'schema.sql')
    with open(schema_path, encoding='utf-8') as f:
        db.executescript(f.read())


from .user import User
from .lot import Lot
from .record import Record
