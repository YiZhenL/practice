import os

class Config:
    # 用於保護應用的資料（例如 CSRF 保護、Session 等），從環境變數中獲取 SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # 資料庫的 URI 配置，用於連接應用程式所需的資料庫，從環境變數中獲取資料庫連結
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # 電子郵件伺服器的主機地址，這裡使用 Gmail 的 SMTP 伺服器
    MAIL_SERVER = 'smtp.googlemail.com'
    
    # 電子郵件伺服器的連接埠，587 是 Gmail SMTP 伺服器的 TLS 連接埠
    MAIL_PORT = 587
    
    # 啟用 TLS（傳輸層安全性），用於加密電子郵件傳輸
    MAIL_USE_TLS = True
    
    # 電子郵件登入用的使用者名稱，從環境變數中獲取電子郵件帳戶
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    
    # 電子郵件登入用的密碼，從環境變數中獲取電子郵件密碼
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
