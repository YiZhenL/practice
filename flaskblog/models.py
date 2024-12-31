from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

# 設置用於加載用戶的方法，Flask-Login 使用此方法來獲取用戶對象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # 根據用戶 ID 從資料庫查找用戶

# User 模型，用於表示應用中的用戶
class User(db.Model, UserMixin):
    # 用戶唯一的 ID 作為主鍵
    id = db.Column(db.Integer, primary_key=True)
    # 用戶名，要求唯一且非空
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 用戶的電子郵件，要求唯一且非空
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 用戶的個人頭像檔案名稱，預設為 "default.jpg"
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # 用戶的密碼（已雜湊）
    password = db.Column(db.String(60), nullable=False)
    # 用戶發佈的文章（與 Post 模型建立關係）
    posts = db.relationship('Post', backref='author', lazy=True)

    # 生成密碼重置令牌，有效期默認為 1800 秒（30 分鐘）
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # 驗證密碼重置令牌
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # 嘗試從令牌中解碼出用戶 ID
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # 定義用戶物件的字串表示
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Post 模型，用於表示用戶的貼文
class Post(db.Model):
    # 貼文唯一的 ID 作為主鍵
    id = db.Column(db.Integer, primary_key=True)
    # 貼文標題，要求非空，最多 100 字
    title = db.Column(db.String(100), nullable=False)
    # 發佈日期，默認為當前時間
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 貼文內容，要求非空
    content = db.Column(db.Text, nullable=False)
    # 與用戶建立關聯（外鍵 user.id）
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 定義貼文物件的字串表示
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
