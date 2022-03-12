from api.sign import app

@app.route('/signup',methods=['GET'])
def signup_form():
    '''注册页面'''
    return'''<!DOCTYPE html>
              <html>
              <body>
              	<h2>注册成为 Bangumoe 会员</h2>
              	<p>一起来moe吧 _(:з」∠)_ </p>
              </body>
              </html>
              <form action="/signup" method="POST">
              <p>你的email地址：</p>
              <p><input name="username"></p>
              <p>设置一个密码：</p>
              <p><input name="password" type="password"></p>
              <p>确认密码：</p>
              <p><input name="password_re" type="password"></p>
              <p>设置一个昵称：</p>
              <p><input name="nickname"></p>
              <p><button type="submit">注册会员</button></p>
              </form>
              <p>已经注册过 Bangumoe 账户？<a href="http://127.0.0.1:5000/login">立即登录</a></p>'''

@app.route('/login',methods=['GET'])
def signin_form():
    '''登录页面'''
    return'''<!DOCTYPE html>
              <html>
              <body>
              	<h2>登录至 Bangumoe</h2>
              </body>
              </html>
              <form action="/signup" method="POST">
              <p>你的email地址：</p>
              <p><input name="username"></p>
              <p>你的密码：</p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">登录</button></p>
              </form>
              <p>还没有 Bangumi 账户？<a href="http://127.0.0.1:5000/signup">立即注册</a></p>'''

if __name__=='__main__':
    app.run()