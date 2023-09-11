from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime
import os
import hashlib

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'User({self.first_name}, {self.email})'


def make_hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    print(salt + key)
    return salt + key


def extract_password(hash_password):
    return hash_password[:32], hash_password[32:]


def verify_password(password_to_verify, stored_password):
    salt, key = stored_password
    new_key = hashlib.pbkdf2_hmac('sha256', password_to_verify.encode('utf-8'), salt, 100_000)
    if new_key == key:
        return True
    else:
        return False


def add_user(user_dict):
    pass_hash = make_hash_password(user_dict.get('password'))
    user = User(
        first_name=user_dict.get('first_name'),
        last_name=user_dict.get('last_name'),
        email=user_dict.get('email'),
        password=pass_hash,
    )
    db.session.add(user)
    db.session.commit()
    return f"Пользователь {user_dict.get('first_name')} {user_dict.get('last_name')} добавлен в БД"
