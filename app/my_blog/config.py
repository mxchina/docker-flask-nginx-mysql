# coding=utf-8
import os
from datetime import timedelta

DEBUG = True

QUESTIONS_PER_PAGE = 3
ANSWER_PER_PAGE = 10
HOMEPAGE_DETAIL_PER_PAGE = 50
HOMEPAGE_TITLE_PER_PAGE = 20
#上传图片需要web服务器ip或者域名
SERVICE_NAME_ = '172.16.10.88'

SECRET_KEY = os.urandom(24)
#设置session过期时间，需要同时在login函数中设置session.permanent = True
PERMANENT_SESSION_LIFETIME = timedelta(days=3)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Mx560205@mysql:3306/myflask?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False

