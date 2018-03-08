# coding=utf-8
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.dialects.mysql import MEDIUMTEXT

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    nickname = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        self.telephone = kwargs.get('telephone')
        self.username = kwargs.get('username')
        self.nickname = kwargs.get('nickname')
        self.password = generate_password_hash(kwargs.get('password'))

    def check_password(self,login_password):
        result = check_password_hash(self.password,login_password)
        return result


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.TEXT,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref = db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    answer_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    user_answer = db.relationship('User',backref = db.backref('answer'))
    question_answer = db.relationship('Question',backref = db.backref('answer'))

class Upload_image(db.Model):
    _tablename_ = 'upload_image'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    addr = db.Column(db.String(200),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    image_tag = db.Column(db.String(30),nullable=False)
    image_md5 = db.Column(db.String(32),nullable=False)

    user_images = db.relationship('User',backref = db.backref('images'))
