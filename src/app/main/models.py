' SQLAlchemy模型类 '

__author__ = 'YiNN'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# 设置数据库的链接信息
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

class Info(db.Model):
    __tablename__ = "info"
    uid = db.Column(db.Integer, primary_key=True,autoincrement=True)
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

class clientCode(db.Model):
    __tablename__ = "clientcode"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    clientID = db.Column(db.String(255),nullable=False)
    code = db.Column(db.String(255))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

