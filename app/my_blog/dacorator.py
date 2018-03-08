# coding=utf-8
from functools import wraps
from flask import session,redirect,url_for
from models import User
import hashlib
import os

#登录限制装饰器
def login_limit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        session_user_id = session.get('user_id')
        if session_user_id:
            user = User.query.filter(User.id == session_user_id).first()
            if user:
                return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

def get_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path,'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5


