'''
⽤⼾的信息⾄少包括
⽤⼾名、密码、邮箱、昵称、头像、简介。
'''

class User(object):
    '''用户模型'''

    def __init__(self,name='',password_hash='',email='',nickname=''):
        self.name=name
        self.__password_hash=password_hash
        self.__email=email
        self.__nickname=nickname
