from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# 定義藍圖，用於將用戶相關的路由組織起來
users = Blueprint('users', __name__)


# 註冊路由
@users.route("/register", methods=['GET', 'POST'])
def register():
    # 如果用戶已經登入，則重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # 驗證表單提交的數據
    if form.validate_on_submit():
        # 雜湊處理用戶的密碼以保護數據
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 創建新用戶
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()  # 將新用戶存入資料庫
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))  # 重定向到登入頁面
    return render_template('register.html', title='Register', form=form)


# 登入路由
@users.route("/login", methods=['GET', 'POST'])
def login():
    # 如果用戶已登入，則重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # 查詢資料庫中對應的用戶
        user = User.query.filter_by(email=form.email.data).first()
        # 驗證密碼是否正確
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # 設置登入狀態
            # 如果用戶訪問受保護路由前請求的頁面，則重定向到該頁面
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# 登出路由
@users.route("/logout")
def logout():
    logout_user()  # 清除用戶登入狀態
    return redirect(url_for('main.home'))


# 用戶帳號管理路由
@users.route("/account", methods=['GET', 'POST'])
@login_required  # 確保只有登入的用戶才能訪問
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # 處理用戶頭像上傳
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # 更新用戶名和電子郵件
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))  # 防止表單重新提交
    elif request.method == 'GET':
        # 預填表單數據
        form.username.data = current_user.username
        form.email.data = current_user.email
    # 加載用戶頭像
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# 用戶貼文路由
@users.route("/user/<string:username>")
def user_posts(username):
    # 獲取分頁參數（預設第 1 頁）
    page = request.args.get('page', 1, type=int)
    # 查找指定用戶
    user = User.query.filter_by(username=username).first_or_404()
    # 查詢用戶的貼文並按發佈日期排序
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


# 密碼重置請求路由
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # 如果用戶已登入，則重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # 查找用戶並發送重置密碼的電子郵件
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# 密碼重置令牌處理路由
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # 如果用戶已登入，則重定向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # 驗證重置令牌是否有效
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 更新用戶的密碼
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
