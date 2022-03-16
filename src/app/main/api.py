' ⽤⼾注册登录 & OAuth2.0 API '

__author__ = 'YiNN'

import json
import random
import string

from app import config
from app.form import *
from app.main.models import Codedata, Info, OAuth, Users
from app.main.token import check_token, generate_token
from flask import Flask, Response, jsonify, make_response, redirect, render_template, request
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

def jsonResponseFactory(data):
    '''Return a callable in top of Response'''
    def callable(response=None, *args, **kwargs):
        '''Return a response with JSON data from factory context'''
        return Response(json.dumps(data), *args, **kwargs)
    return callable

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
                codedata = Codedata(code = code_,uemail=email,uid=user.uid)
                db.session.add(codedata)
                db.session.commit()
                response_info = {'code': code_}
                return redirect(
                        redirect_url,
                        302,
                        jsonResponseFactory(response_info)
                    )
            else:
                return jsonify(msg='user id/password error')
        else:
            return jsonify(msg='clientID or backURL error')
    else:
        form = LoginForm()
        return render_template("login.html",form=form)

@app.route('/oauth2.0/granttoken', methods=['POST', 'GET'])
def oauthgranttoken():
    '''生成token的api'''
    client_id=request.json.get("client_id")
    client_secrets=request.json.get("client_secrets")
    code=request.json.get("code")
    oauth=OAuth.query.filter(OAuth.clientID==client_id).first()
    if not oauth :
        return jsonify(msg='client id error')
    result = check_password_hash(oauth.secrets,client_secrets)
    if not result:
        return jsonify(msg='client secrets error')
    codedata = Codedata.query.filter(Codedata.code==code).first()
    if codedata:
        data={}
        data['email']=codedata.uemail
        data['uid']=codedata.uid
        token=generate_token(data)
        return jsonify({'token':token})
    else:
        return jsonify(msg='code异常')

@app.route('/oauth2.0/getinfo', methods=['POST', 'GET'])
def oauthgetinfo():
    '''获取用户信息的API'''
    token=request.json.get("token")
    result=check_token(token)
    if result:
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
    else:
        return jsonify(msg='token异常')

if __name__=='__main__':
    app.run()
