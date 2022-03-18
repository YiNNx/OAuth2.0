' 生成与验证token的函数 '

__author__ = 'YiNN'

from typing import Dict
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from itsdangerous import BadData

def generate_code(id):
    """ 生成code，有效期600s """
    secret_key= 'afesjyrtrw6457t'
    expires_in = 600
    serializer = TJWSSerializer(secret_key, expires_in )	
    token = serializer.dumps(id)   
    token = token.decode()   
    return token

def check_code(token):
    secret_key= 'afesjyrtrw6457t'
    expires_in = 600
    serializer = TJWSSerializer(secret_key, expires_in )
    try:
        id = serializer.loads(token)
    except BadData:
        return None
    else:
        return id


def generate_token(data:Dict):
	""" 生成token """
	secret_key= 'afesjyrtrw6457t'
	serializer = TJWSSerializer(secret_key)
	token = serializer.dumps(data)   # data为要加密的数据
	token = token.decode()   # 得到返回后的带有效期和用户信息的加密token
	
	return token


# 检验token(secret和有效期(expires_in)需要与生成时一致)
def check_token(token):
    secret_key= 'afesjyrtrw6457t'
    serializer = TJWSSerializer(secret_key)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('uid')
        user_email = data.get('email')
        return [user_id,user_email]

def generate_user_active_token(id):
    """ 生成用户邮箱验证token，有效期十分钟 """
    secret_key= 'afesjyrtrw6457t'
    expires_in = 600 
    serializer = TJWSSerializer(secret_key, expires_in )	
    token = serializer.dumps(id)   
    token = token.decode()   
    return token

def check_user_active_token(token):
    """ 验证用户邮箱验证token，有效期十分钟 """
    secret_key= 'afesjyrtrw6457t'
    expires_in = 600
    serializer = TJWSSerializer(secret_key, expires_in )
    try:
        id = serializer.loads(token)
    except BadData:
        return None
    else:
        return id

if __name__=='__main__':
    '''test'''
    data={}
    data['uid']='345'
    data['email']='123'
    token=generate_token(data)
    print(token)
    check=check_token(token)
    print(check)
    id=3
    token=generate_user_active_token(id)
    result=check_user_active_token(token)
    print(token)
    print(result)
