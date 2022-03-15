' 生成token与code的函数 '

__author__ = 'YiNN'

from typing import Dict
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from itsdangerous import BadData

secret_key= 'afesjyrtrw6457t'
expires_in = 360   # 有效期单位为秒

def generate_code(data:Dict):
	""" 生成code """
	# serializer = TJWSSerializer(秘钥, 有效期单位为秒)
	serializer = TJWSSerializer(secret_key, expires_in )
	
	# serializer.dumps(数据), 返回bytes类型，比如对用户的id和email进行加密返回前端

	token = serializer.dumps(data)   # data为要加密的数据
	token = token.decode()   # 得到返回后的带有效期和用户信息的加密token
	
	return token


# 检验token(secret和有效期(expires_in)需要与生成时一致)
def check_token(token):
	# 验证失败，会抛出itsdangerous.BadData异常
    serializer = TJWSSerializer(secret_key, expires_in )
    try:
		# 获取解密后的数据 bytes:dict
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('id')
        user_email = data.get('email')
        try:
            user = User.objects.get(id=user_id,email=user_email)
        except User.DoesNotExist:
            return None
        else:
        	return user

