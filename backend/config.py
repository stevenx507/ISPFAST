import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ispmax.db')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true') == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'info@ispmax.com')
    MIKROTIK_HOST = os.getenv('MIKROTIK_HOST', '192.168.88.1')
    MIKROTIK_USER = os.getenv('MIKROTIK_USER', 'admin')
    MIKROTIK_PASS = os.getenv('MIKROTIK_PASS', '')
    MIKROTIK_PORT = int(os.getenv('MIKROTIK_PORT', 8728))
    MIKROTIK_USE_SSL = os.getenv('MIKROTIK_USE_SSL', 'false') == 'true'
    PARAM_BURST_MULTIPLIER = 1.5
    PARAM_TIMEOUT = '30s'
    PARAM_MIN_SPEED = 50
    PARAM_MAX_SPEED = 500
    PARAM_PRICE_PER_MB = 4.5  # MXN por Mbps
