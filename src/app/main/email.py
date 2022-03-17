from flask import Flask,render_template
from flask_mail import Mail,Message
import config


app = Flask(__name__)
app.config.from_object(config)

mail = Mail()
mail.init_app(app)

#发送文本
@app.route('/verify')
def email_send_charactor():
    message = Message(subject='verify your email',recipients=['2436201947@qq.com'],body='你的验证码为%s'%veri)
    try:
        mail.send(message)
        return 'ok'
    except Exception as e:
        print(e)
        return 'error'

if __name__ == '__main__':
    app.run(debug=True)