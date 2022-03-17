from flask import Flask, render_template
from flask_mail import Mail,Message

import config
'''pzjcwwbgknrkgaee'''
app = Flask(__name__)
app.config.from_object(config)


def send_email(to, subject, template, **kwargs):
    body = 'test' # 注意此处调用的模板渲染
    mes = Message(subject,recipients=[to],body=body)
    mail.send(mes)
# 调用如下



mail = Mail(app)
@app.route('/email_send')
def email_send():
    body = 'test' # 注意此处调用的模板渲染
    mes = Message('test',recipients=['2436201947'],body=body)
    mail.send(mes)
    #send_email('2436201947', '注册确认邮件','confirm')
    return '发送成功，请注意查收'


if __name__=='__main__':
    app.run(debug=True) 