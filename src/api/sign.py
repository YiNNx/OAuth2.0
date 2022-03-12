'''
实现最基本的⽤⼾注册登录和修改信息的API。
'''

from .app import app
from .models import User
from flask import request

@app.route('/signup',methods=['POST'])
def signup():
    if request.form:
        u=User(request.form['username'],request.form['password'])
    return """succeed!"""

@app.route('/login',methods=['post'])
def login():
    if request.form:
        pass

if __name__=='__main__':
    app.run()