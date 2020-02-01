from secrets import token_hex


class Config:
    ENV = "production"
    SECRET_KEY = token_hex()
    # DATABASE
    DB_NAME = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_HOST = "127.0.0.1"
    # SMTP
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = ""
    RECEIVER_EMAIL = ""
    EMAIL_PASSWORD = ""
