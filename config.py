import os

class Config:
    SECRET_KEY = 'your_secret_key'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path to your project directory
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "databases", "main.db")}'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'iwilllive.agoodlife97@gmail.com'
    MAIL_PASSWORD = 'tcpv jnyn nyqe kxaq'
