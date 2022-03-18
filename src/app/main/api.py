' ⽤⼾注册登录 & OAuth2.0 API '

__author__ = 'YiNN'

import json
import random
import string

import http
from app import config
from app.main.form import *
from app.main.get_collection import *
from app.main.models import Anime,  Collection, Info, OAuth, Users
from app.main.generate import check_code, check_token, check_user_active_token, generate_code, generate_token, generate_user_active_token
from flask import Flask, Response, jsonify,  redirect, render_template, request, session
from flask_mail import Mail,Message
from urllib import parse as url_parse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

APP_ID = 'bgm22106232fa6225d8a'
APP_SECRET = '7402491845d1b66ce1360c33293b472a'
WEBSITE_BASE = 'http://http://127.0.0.1:5000/'
CALLBACK_URL = 'http://127.0.0.1:5000/oauth/redirect'
USER_AUTH_URL = 'https://bgm.tv/oauth/authorize?' + url_parse.urlencode({
    'client_id': APP_ID,
    'response_type': 'code',
    'redirect_uri': CALLBACK_URL,
})

app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)

db = SQLAlchemy(app)

mail = Mail()
mail.init_app(app)

'''邮箱验证'''

def send_email(uid,uemail):
    token=generate_user_active_token(uid)
    body='请点击地址进行邮箱验证 http://127.0.0.1:5000/verify/%s'%token
    message = Message(subject='欢迎加入 Bangumoe！',recipients=[uemail],body=body)
    try:
        mail.send(message)
        print('succeed')
    except Exception as e:
        print(e)
        return jsonify(msg='邮件发送失败')

@app.route('/verify/<token>')
def verify(token):
    uid=check_user_active_token(token)
    user = Users.query.filter(Users.uid==uid).first()
    if user:
        user.statu=1
        db.session.merge(user)
        db.session.commit()
        session['uid']=user.uid
        return '''<h2>创建账号成功！</h2>
                  <p><a href="http://127.0.0.1:5000/">主页</a></p>'''
    else:
        return jsonify(msg='token-time-out')

'''⽤⼾注册登录和修改信息'''

@app.route('/')
def index():
    if 'uid' in session:
        return render_template("home.html")
    else:
        return render_template("index.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    '''注册页面'''
    if 'uid' in session:
        return redirect('http://127.0.0.1:5000/')
    if request.method =="GET":
        form = SignUpForm()
        return render_template("signup.html",form=form)
    else:
        form = SignUpForm(formdata=request.form)
        if form.validate(): 
            pword_h=generate_password_hash(form.data['pword'])
            user = Users(
                email = form.data['email'],
                pword_hash = pword_h,
                uname = form.data['email']
                )
            try:
                db.session.add(user)
                db.session.commit()
                user = Users.query.filter(Users.email==form.data['email']).first()
                uinfo = Info(
                    uid=user.uid,
                    email = form.data['email'],
                    uname = form.data['email'],
                    nickname=form.data['nickname']
                    )
                db.session.add(uinfo)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify(msg='注册失败,请检查你的邮箱是否注册过账号')
            '''接下来进行邮箱验证'''
            send_email(user.uid,user.email)
            return '''<h2>激活 Bangumoe 账户</h2>
                    感谢注册 Bangumoe，在开始使用前你需要激活你的 Bangumoe 账户。
                    包含激活链接的邮件已发送至 %s（有效期为10分钟）。请根据邮件提示进行激活操作。'''%user.email
        else:
            print(form.errors,"错误信息")
        return render_template("signup.html",form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    '''登录页面'''
    if session.get('uid'):
        return redirect('http://127.0.0.1:5000/')
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
                if user.statu==0:
                    return "该账户未激活"
                session['uid'] = user.uid
                return '''<h2>登录成功！</h2>
	                      <p><a href="http://127.0.0.1:5000/">主页</a></p>'''
            else:
                return jsonify(msg='用户名或密码错误')
        return render_template("login.html",form=form)

@app.route("/logout", methods=["GET"])
def logout():
    """退出登录"""
    # 清空session
    session.clear()
    return redirect('http://127.0.0.1:5000/')

@app.route('/info',methods=['GET','POST'])
def info():
    '''info页面'''
    if 'uid' in session:
        if request.method =="GET":
            form = InfoForm()
            return render_template("info.html",form=form)
        else:
            form = InfoForm(formdata=request.form)
            if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
                print(form.data)
                info = Info.query.filter(Info.email==form.data['email']).first()
                if info.uid!=session['uid']:
                    return jsonify(msg='email错误')
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
                    return jsonify(msg='修改失败,请检查你的邮箱是否正确')
                return jsonify(msg="修改成功")
            else:
                print(form.errors,"错误信息")
            return jsonify(msg="输入异常")
    else:
        return '''<p>请先<a href="http://127.0.0.1:5000/login">登录</a></p>'''


'''OAuth2.0 Client'''

@app.route('/oauth/login')
def oauth_login():
    return redirect(USER_AUTH_URL)

@app.route('/oauth/redirect')
def oauth_callback():
    code = request.args.get('code')
    conn = http.client.HTTPSConnection("bgm.tv")
    payload = json.dumps({
      "grant_type": "authorization_code",
      "client_id": APP_ID,
      "client_secret": APP_SECRET,
      "code": code,
      "redirect_uri": CALLBACK_URL
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'chii_sec_id=O42uIqoA4WwTds0aDtt4UXbic3GrzTcsu8vIDhm9; chii_sid=1OoXmD'
    }
    conn.request("POST", "/oauth/access_token", payload, headers)
    res = conn.getresponse()
    raw_data = res.read()
    encoding = res.info().get_content_charset('utf8')
    data = json.loads(raw_data.decode(encoding))
    access_token=data['access_token']
    '''获得token，进行用户数据导入'''
    uid=session['uid']
    user = Users.query.filter(Users.uid==uid).first()
    user.access_token=access_token
    db.session.merge(user)
    db.session.commit()
    try:
        load_data(uid,access_token)
    except Exception as e:
        return '''账号绑定成功！但数据导入似乎出现了一些问题'''
    return '''账号绑定成功！<a href="http://127.0.0.1:5000/collection">查看我的收藏</a>'''

def load_data(uid,access_token):
    '''载入用户番剧数据'''
    data=get_collections(access_token)
    datalist=data['data']
    for item in datalist:
        collection=Collection(
            uid=uid,
            name=get_anime_name(item['subject_id']),
            statu=switch_type(item['type']),
            score=item['rate'],
            comment=item['comment']
        )
        try:
            db.session.add(collection)
            db.session.commit()
            print('loading succeed!')
        except Exception as e:
            db.session.rollback()
            print('loading failed')


'''OAuth2.0 Server'''

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
                return jsonify(msg='注册失败')
            return "成功！你的Client ID为 %s"%cid
        else:
            print(form.errors,"错误信息")
        return render_template("oauth_sign.html",form=form)

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
            if not user:
                return jsonify(msg='user email error')
            result = check_password_hash(user.pword_hash,password)
            if result:
                code_=generate_code(user.uid)
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
    codedata = check_code(code)
    user=Users.query.filter(Users.uid==codedata).first()
    if user:
        data={}
        data['email']=user.email
        data['uid']=user.uid
        token=generate_token(data)
        return jsonify({'token':token})
    else:
        return jsonify(msg='code异常',code=code,codedata=codedata)

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


''' 番剧收藏&搜索 '''

@app.route('/anime', methods=['POST', 'GET'])
def allanimes():
    if request.method =="GET":
        animes = Anime.query.filter().all()
        return render_template('allanimes.html',animes=animes)
    else:
        content = request.form.get('content')
        animes = Anime.query.filter(Anime.name.contains(content)).all()
        return render_template('allanimes.html',animes=animes)
    
@app.route('/anime/<name>', methods=['POST', 'GET'])
def animeshow(name):
    anime = Anime.query.filter(Anime.name==name).first()
    session['anime']=name
    if not anime:
        return jsonify(msg='page not found')
    return render_template('anime.html',anime=anime)

@app.route('/collecting', methods=['POST', 'GET'])
def collectit():
    if request.method =="GET":
        if not session.get('anime'):
            return jsonify(msg='page not found')
        if not session.get('uid'):
            return '请先<a href="http://127.0.0.1:5000/login">登录</a>'
        form=CollectForm()
        name=session['anime']
        return render_template('collecting.html',name=name,form=form)
    else:
        form = CollectForm(formdata=request.form)
        if form.validate():
            collection=Collection.query.filter(Collection.uid==session['uid'], Collection.name == session['anime']).first()
            if not collection:
                collection = Collection(
                    uid = session['uid'],
                    name = session['anime'],
                    statu = form.data['statu'],
                    score = form.data['score'],
                    comment = form.data['comment']
                    )
                try:
                    db.session.add(collection)
                    db.session.commit()
                    print('succeed!')
                except Exception as e:
                    db.session.rollback()
                    return jsonify(msg='收藏失败')
                return """收藏成功！<a href="http://127.0.0.1:5000/collection">查看我的收藏</a>"""
            else:
                collection.statu = form.data['statu']
                collection.score = form.data['score']
                collection.comment = form.data['comment']
                try:
                    db.session.merge(collection)
                    db.session.commit()
                    print('succeed!')
                except Exception as e:
                    db.session.rollback()
                    return jsonify(msg='收藏失败')
                return """修改成功！<a href="http://127.0.0.1:5000/collection">查看我的收藏</a>"""
        else:
            print(form.errors,"错误信息")

            #session.pop('anime')
            return jsonify(msg='收藏失败')

@app.route('/collection', methods=['POST', 'GET'])
def anime():
    if request.method =="GET":
        if not session.get('uid'):
            return jsonify(msg='请先登录')
        collection = Collection.query.filter(Collection.uid==session['uid']).all()
        print(collection)
        return render_template('collection.html',collections=collection)
    else:
        content = request.form.get('content')
        collection = Collection.query.filter(Collection.name.contains(content)).all()
        return render_template('collection.html',collections=collection)

if __name__=='__main__':
    app.run()
