#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 实现最基本的⽤⼾注册登录和修改信息的API。 '

__author__ = 'YiNN'

#from ..models import User
from flask import Flask,render_template, request, flash
from app.main.form import *
from .. import config


app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)

@app.route('/')
def hello_world():
    flash('welcome')
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
            print("用户提交的数据用过格式验证，值为：%s"%form.data)
            return "登录成功"
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
            print("用户提交的数据用过格式验证，值为：%s"%form.data)
            return "登录成功"
        else:
            print(form.errors,"错误信息")
        return render_template("login.html",form=form)

if __name__=='__main__':
    app.run()