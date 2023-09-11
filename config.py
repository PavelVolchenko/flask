import secrets


class Config(object):
    SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = secrets.token_hex()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
