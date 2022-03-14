' 实现最基本的⽤⼾注册登录和修改信息的API。 '

__author__ = 'YiNN'

from flask import Flask,render_template, request
from app.form import *
from app import config
from app.main.models import Info, Users #,db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup',methods=['GET','POST'])
def signup_form():
    '''注册页面'''
    if request.method =="GET":
        form = SignUpForm()
        return render_template("signup.html",form=form)
    else:
        form = SignUpForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            #print(form.data)
            pword_h=generate_password_hash(form.data['pword'])
            user = Users(email = form.data['email'],pword_hash = pword_h,uname = form.data['email'])
            uinfo = Info(email = form.data['email'],uname = form.data['email'],nickname=form.data['nickname'])
            try:
                db.session.add(user)
                db.session.add(uinfo)
                db.session.commit()
                print('succeed!')
            except Exception as e:
                db.session.rollback()
                return '注册失败,请检查你的邮箱是否注册过账号'
            return render_template("info_signup.html")
        else:
            print(form.errors,"错误信息")
        return render_template("signup.html",form=form)

@app.route('/login',methods=['GET','POST'])
def login_form():
    '''登录页面'''
    if request.method =="GET":
        form = LoginForm()
        return render_template("login.html",form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            #print(form.data)
            user = Users.query.filter(Users.email==form.data['email']).first()
            result = check_password_hash(user.pword_hash,form.data['pword'])
            if result:
                return render_template("info_login.html")
            else:
                return '用户名或密码错误'
        else:
            print(form.errors,"错误信息")
        return render_template("login.html",form=form)


@app.route('/info',methods=['GET','POST'])
def info_form():
    '''info页面'''
    if request.method =="GET":
        form = InfoForm()
        return render_template("info.html",form=form)
    else:
        form = InfoForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            print(form.data)
            info = Info.query.filter(Info.email==form.data['email']).first()
            print(info.email)
            print(info.avator)
            try:
                info.nickname = form.data['nickname']
                info.avator = form.data['avator']
                info.intro = form.data['intro']
                print(info.nickname,info.avator,info.intro)
                db.session.merge(info)
                db.session.commit()
                print('succeed!')
            except Exception as e:
                db.session.rollback()
                return '修改失败,请检查你的邮箱是否正确'
            return "修改成功"
        else:
            print(form.errors,"错误信息")
        return "输入异常"

if __name__=='__main__':
    app.run()