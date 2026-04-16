from flask import Blueprint

# 註冊所有的 Blueprints 可以集中在這裡，方便 app.py 引入
from .main import main_bp
from .auth import auth_bp
from .fortune import fortune_bp
from .donate import donate_bp

def init_app(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(fortune_bp, url_prefix='/fortune')
    app.register_blueprint(donate_bp, url_prefix='/donate')
