from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# 初始化資料庫（SQLAlchemy 用於 ORM 操作）
db = SQLAlchemy()
# 初始化密碼加密模組（Bcrypt 用於密碼雜湊）
bcrypt = Bcrypt()
# 初始化登入管理（Flask-Login）
login_manager = LoginManager()
# 設定登入頁面的端點（未登入時會重定向至此）
login_manager.login_view = 'users.login'
# 設定登入訊息分類（用於 Flash 消息顯示）
login_manager.login_message_category = 'info'
# 初始化電子郵件模組（Flask-Mail）
mail = Mail()

# 應用程式工廠模式
def create_app(config_class=Config):
    # 創建 Flask 應用實例
    app = Flask(__name__)
    # 載入配置
    app.config.from_object(Config)

    # 初始化各模組與 Flask 應用的綁定
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # 匯入並註冊藍圖（Blueprints）以模組化應用程式
    from flaskblog.users.routes import users  # 用戶相關路由
    from flaskblog.posts.routes import posts  # 貼文相關路由
    from flaskblog.main.routes import main    # 主頁相關路由
    from flaskblog.errors.handlers import errors  # 錯誤處理相關路由
    app.register_blueprint(users)  # 註冊用戶藍圖
    app.register_blueprint(posts)  # 註冊貼文藍圖
    app.register_blueprint(main)   # 註冊主頁藍圖
    app.register_blueprint(errors) # 註冊錯誤處理藍圖

    # 返回應用實例
    return app
