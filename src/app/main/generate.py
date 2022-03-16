' 生成与验证token的函数 '

__author__ = 'YiNN'

from typing import Dict
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from itsdangerous import BadData

def generate_token(data:Dict):
	""" 生成token """
	secret_key= 'afesjyrtrw6457t'
	expires_in = 600 
	# serializer = TJWSSerializer(秘钥, 有效期单位为秒)
	serializer = TJWSSerializer(secret_key, expires_in )
	
	# serializer.dumps(数据), 返回bytes类型，比如对用户的id和email进行加密返回前端

	token = serializer.dumps(data)   # data为要加密的数据
	token = token.decode()   # 得到返回后的带有效期和用户信息的加密token
	
	return token


# 检验token(secret和有效期(expires_in)需要与生成时一致)
def check_token(code):
	# 验证失败，会抛出itsdangerous.BadData异常
    secret_key= 'afesjyrtrw6457t'
    expires_in = 600
    serializer = TJWSSerializer(secret_key, expires_in )
    try:
		# 获取解密后的数据 bytes:dict
        data = serializer.loads(code)
    except BadData:
        return None
    else:
        user_id = data.get('uid')
        user_email = data.get('email')
        return [user_id,user_email]

if __name__=='__main__':
    '''test'''
    data={}
    data['uid']='345'
    data['email']='123'
    token=generate_token(data)
    print(token)
    check=check_token(token)
    print(check)
