' wtf表单 '

__author__ = 'YiNN'

from wtforms.fields import simple
from wtforms import Form,validators,widgets

class LoginForm(Form):
    '''Form'''
    email = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ"),
            validators.Email(message="请输入正确的Email格式(ﾟДﾟ*)ﾉ"),
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

    pword = simple.PasswordField(
        validators=[
            validators.DataRequired(message="请输入密码(ﾟДﾟ*)ﾉ"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class":"form-control"}
    )

class SignUpForm(Form):
    '''Form'''
    email = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ"),
            validators.Email(message="请输入正确的Email格式(ﾟДﾟ*)ﾉ"),
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

    pword = simple.PasswordField(
        validators=[
            validators.DataRequired(message="请输入密码(ﾟДﾟ*)ﾉ"),
            validators.Length(max=20,min=6,message="密码长度须大于%(max)d字且小于%(min)d字(ﾟДﾟ*)ﾉ"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class":"form-control"}
    )

    pword_re = simple.PasswordField(
        validators=[
            validators.DataRequired(message="请输入密码(ﾟДﾟ*)ﾉ"),
            validators.EqualTo('pword',message="两次密码输入不同哦(ﾟДﾟ*)ﾉ"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class":"form-control"}
    )

    nickname = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ"),
            validators.Length(max=8,min=3,message="昵称须大于%(max)d字且小于%(min)d字(ﾟДﾟ*)ﾉ")
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

class InfoForm(Form):
    '''Form'''
    
    email = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ"),
            validators.Email(message="请输入正确的Email格式(ﾟДﾟ*)ﾉ"),
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

    nickname = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ"),
            validators.Length(max=8,min=3,message="昵称须大于%(max)d字且小于%(min)d字(ﾟДﾟ*)ﾉ")
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

    avator = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ")
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

    intro = simple.StringField(
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="不能为空(ﾟДﾟ*)ﾉ"),
        ],
        render_kw={"class":"form-control"}  #设置属性生成的html属性
    )

    