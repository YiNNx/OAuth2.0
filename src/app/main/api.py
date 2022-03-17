' ⽤⼾注册登录 & OAuth2.0 API '

__author__ = 'YiNN'

import json
import random
import string

from app import config
from app.main.form import *
from app.main.models import Anime, Codedata, Collection, Info, OAuth, Users
from app.main.generate import check_token, check_user_active_token, generate_token
from flask import Flask, Response, jsonify,  redirect, render_template, request, session
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)

db = SQLAlchemy(app)

mail = Mail()
mail.init_app(app)

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
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            pword_h=generate_password_hash(form.data['pword'])
            print(form.data)
            user = Users(email = form.data['email'],pword_hash = pword_h,uname = form.data['email'])
            try:
                db.session.add(user)
                db.session.commit()
                print('succeed!')
                session['uid'] = user.uid
            except Exception as e:
                db.session.rollback()
                return '注册失败,请检查你的邮箱是否注册过账号'
            try:
                user = Users.query.filter(Users.email==form.data['email']).first()
                print(user.uid)
                uinfo = Info(uid=user.uid,email = form.data['email'],uname = form.data['email'],nickname=form.data['nickname'])
                db.session.add(uinfo)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return '注册失败'
            return '''<h2>创建账号成功！</h2>
                      <p><a href="http://127.0.0.1:5000/">主页</a></p>'''
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
                session['uid'] = user.uid
                return '''<h2>登录成功！</h2>
	                      <p><a href="http://127.0.0.1:5000/">主页</a></p>'''
            else:
                return '用户名或密码错误'
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
                    return 'email错误'
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
    else:
        return '''<p>请先<a href="http://127.0.0.1:5000/login">登录</a></p>'''


'''邮箱验证'''

@app.route('/verify')
def email_send_charactor():
    message = Message(subject='verify your email',recipients=['2436201947@qq.com'],body='你的验证码为%s'%veri)
    try:
        mail.send(message)
        return 'ok'
    except Exception as e:
        print(e)
        return 'error'

@app.route('/verify/<token>')
def verify(token):
    uid=check_user_active_token(token)
    if uid==session.get('uid'):
        pass


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
        return '页面走丢了'
    return render_template('anime.html',anime=anime)

@app.route('/collecting', methods=['POST', 'GET'])
def collectit():
    if request.method =="GET":
        if not session.get('anime'):
            return 'page not found'
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
                    return '收藏失败'
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
                    return '收藏失败'
                return """修改成功！<a href="http://127.0.0.1:5000/collection">查看我的收藏</a>"""
        else:
            print(form.errors,"错误信息")

            #session.pop('anime')
            return '收藏失败'

@app.route('/collection', methods=['POST', 'GET'])
def anime():
    if request.method =="GET":
        if not session.get('uid'):
            return '请先登录'
        collection = Collection.query.filter(Collection.uid==session['uid']).all()
        print(collection)
        return render_template('collection.html',collections=collection)
    else:
        content = request.form.get('content')
        collection = Collection.query.filter(Collection.name.contains(content)).all()
        return render_template('collection.html',collections=collection)

if __name__=='__main__':
    app.run()
