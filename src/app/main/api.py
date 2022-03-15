' 实现最基本的⽤⼾注册登录和修改信息的API。 '

__author__ = 'YiNN'

import random
import string

from app import config
from app.form import *
from app.main.models import Codedata, Info, OAuth, Users, clientCode
from app.main.token import check_token, generate_token
from flask import Flask, jsonify, make_response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)

db = SQLAlchemy(app)

'''⽤⼾注册登录和修改信息'''

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    '''注册页面'''
    if request.method =="GET":
        form = SignUpForm()
        return render_template("signup.html",form=form)
    else:
        form = SignUpForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
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
def login():
    '''登录页面'''
    if request.method =="GET":
        form = LoginForm()
        return render_template("login.html",form=form)
    elif request.method =="POST":
        form = LoginForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            #print(form.data)
            user = Users.query.filter(Users.email==form.data['email']).first()
            result = check_password_hash(user.pword_hash,form.data['pword'])
            if result:
                return render_template("info_login.html")
            else:
                return '用户名或密码错误'
        return render_template("login.html",form=form)


@app.route('/info',methods=['GET','POST'])
def info():
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

'''OAuth2.0'''

@app.route('/oauth2.0/sign',methods=['GET','POST'])
def oauthsign():
    '''oauth注册页面'''
    if request.method =="GET":
        form = OAuthSignForm()
        return render_template("oauth_sign.html",form=form)
    else:
        form = OAuthSignForm(formdata=request.form)
        if form.validate(): 
            secrets_hash=generate_password_hash(form.data['secrets'])
            cid=''.join(random.sample(string.ascii_letters+string.digits,20))
            oauth = OAuth(
                appname = form.data['appName'],
                homeURL = form.data['homeURL'],
                appDesc = form.data['appDesc'],
                backURL = form.data['backURL'],
                secrets = secrets_hash,
                clientID = cid
                )
            try:
                db.session.add(oauth)
                db.session.commit()
                print('succeed!')
            except Exception as e:
                db.session.rollback()
                return '注册失败'
            return "成功！你的Client ID为 %s"%cid
        else:
            print(form.errors,"错误信息")
        return render_template("oauthSign.html",form=form)


@app.route('/oauth2.0/show', methods=['POST', 'GET'])
def oauthshow():
    '''oauth授权页面'''
    if request.get_json():
        client_id=request.json.get("client_id")
        redirect_url=request.json.get("redirect_url")
        oauth=OAuth.query.filter(OAuth.clientID==client_id).first()
        if oauth and oauth.backURL==redirect_url:
            email =request.json.get('email')
            password =request.json.get('password')
            user = Users.query.filter(Users.email==email).first()
            result = check_password_hash(user.pword_hash,password)
            if result:
                code_=''.join(random.sample(string.ascii_letters+string.digits,20))
                clientcode = clientCode(uemail=email,code = code_)
                db.session.add(clientcode)
                db.session.commit()
                response_info = {'code': code_}
                headers = {
                    'content-type':'application/json',
                    'location': redirect_url
                }
                response = make_response(response_info,302)
                response.headers = headers
                return response
            else:
                return jsonify(msg='用户名或密码异常')
        else:
            return jsonify(msg='clientID异常')
    else:
        form = LoginForm()
        return render_template("login.html",form=form)

@app.route('/oauth2.0/granttoken', methods=['POST', 'GET'])
def oauthgranttoken():
    '''token生成api'''
    client_id=request.json.get("client_id")
    client_secrets=request.json.get("client_secrets")
    code=request.json.get("code")
    oauth=OAuth.query.filter(OAuth.clientID==client_id).first()
    result = check_password_hash(oauth.secrets,client_secrets)
    if not oauth or not result:
        return jsonify(msg='client id 或 secrets异常')
    codedata = Codedata.query.filter(Codedata.code==code).first()
    if codedata:
        data={}
        data['email']=codedata.uemail
        data['uid']=codedata.uid
        token=generate_token(data)
        return jsonify({'token':token})
    else:
        return jsonify(msg='code不存在')

@app.route('/oauth2.0/getinfo', methods=['POST', 'GET'])
def oauthgetinfo():
    token=request.json.get("token")
    result=check_token(token)
    uname=result[1]
    info = Info.query.filter(Info.uname==uname).first()
    userInfo = {
        'uname':info.uname,
        'email':info.email,
        'nickname':info.nickname,
        'avator':info.avator,
        'intro':info.intro
    }
    return jsonify(userInfo)

if __name__=='__main__':
    app.run()