' SQLAlchemy模型类 '

__author__ = 'YiNN'

from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ="mysql://root:080502@127.0.0.1:3306/bangumoe"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
	# 指定表名称
    __tablename__ = "users"
    # 主键, 参数1: 表示id的类型, 参数2: 表示id的约束类型
    uid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    uname = db.Column(db.String(32),nullable=False,unique=True)
    email = db.Column(db.String(64),nullable=False,unique=True)
    pword_hash = db.Column(db.String(511),nullable=False,index=True)
    statu = db.Column(db.Integer,nullable=False,default=0)
    access_token = db.Column(db.String(64),default='0')
    
class Info(db.Model):
    __tablename__ = "info"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    uid = db.Column(db.Integer,nullable=False)
    uname = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(511),nullable=False)
    nickname = db.Column(db.String(32),nullable=False)
    avator = db.Column(db.String(64))
    intro = db.Column(db.String(200))

class OAuth(db.Model):
    __tablename__ = "oauth"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    appname = db.Column(db.String(255),nullable=False)
    homeURL = db.Column(db.String(255),nullable=False)
    appDesc = db.Column(db.String(255),nullable=False)
    backURL = db.Column(db.String(255),nullable=False)
    clientID = db.Column(db.String(255))
    secrets = db.Column(db.String(255))

'''class Codedata(db.Model):
    __tablename__ = "codedata"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    code = db.Column(db.String(255),nullable=False)
    uid = db.Column(db.String(255),nullable=False)
    uemail = db.Column(db.String(255),nullable=False)
'''
class Anime(db.Model):
    __tablename__ = "anime"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(64),nullable=False)
    episode=db.Column(db.Integer)
    director=db.Column(db.String(64))

class Collection(db.Model):
    __tablename__='collection'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    uid = db.Column(db.Integer,nullable=False)
    name=db.Column(db.String(64),nullable=False)
    statu=db.Column(db.String(32),nullable=False)
    score=db.Column(db.Integer)
    comment=db.Column(db.String(256))

if __name__ == '__main__':
    #anime=Anime(
    #    name='辉夜大小姐想让我告白 第一季',
    #    episode=12,
    #    director='畠山守'
    #)
    #db.session.add(anime)
    #db.session.commit()
    #db.create_all()
    #app.run(debug=True)
    pass
