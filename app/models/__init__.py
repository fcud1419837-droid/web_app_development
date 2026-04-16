import sqlite3
from flask import g, current_app
import os

def get_db():
    """
    獲取資料庫連線，如果當前 app 上下文中沒有，就建立一個新的。
    """
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE', os.path.join(current_app.instance_path, 'database.db'))
        # 確保資料夾存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    schema_path = os.path.join(current_app.root_path, '..', 'database', 'schema.sql')
    with current_app.open_resource(schema_path) as f:
        db.executescript(f.read().decode('utf8'))
        
from .user import User
from .lot import Lot
from .record import Record
