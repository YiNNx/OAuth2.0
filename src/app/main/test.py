''' test '''

"""""""""

授权界面：
https://bgm.tv/oauth/authorize?client_id=bgm22106232fa6225d8a&response_type=code&redirect_url=http://127.0.0.1:5000/oauth/redirect

https://bgm.tv/oauth/authorize?client_id=bgm22106232fa6225d8a&response_type=code&redirect_uri=http%3A%2F%2Fhttp%3A%2F%2F127.0.0.1%3A5000%2Foauth_callback
回调界面：
http://127.0.0.1:5000/oauth/redirect?code=02db151ca54238923573fb950a313cadbcac17f3


使用返回的的 `code` 换取 Access Token：
{
"grant_type":"authorization_code",
"client_id":"bgm22106232fa6225d8a",
"client_secret":"7402491845d1b66ce1360c33293b472a",
"code":"d155a5d3e278033b32c9d5e3f60c0499ed1bc862",
"redirect_uri":"http://127.0.0.1:5000/oauth/redirect" 
}

{
"access_token":"21d88cc3aeb00495c2d02d8b0d0e18d35406d6a8",
"expires_in":604800,
"token_type":"Bearer",
"scope":null,
"user_id":675222,
"refresh_token":"525e7911d7321fbe708ce4d8d7da6277703f20d6"
}



{"access_token":"852161cadf5a2f706d0477db9b970a7e8a8d24ea","expires_in":604800,"token_type":"Bearer","scope":null,"user_id":675222,"refresh_token":"61f572cebe0807d07d23651235d8fa252a488f81"}
"""
import http.client
import json.decoder
import pathlib
from os import path
from urllib import parse as url_parse

import requests
from flask import Flask, jsonify, redirect, request

APP_ID = 'bgm22106232fa6225d8a'
APP_SECRET = '7402491845d1b66ce1360c33293b472a'
WEBSITE_BASE = 'http://http://127.0.0.1:5000/'

CALLBACK_URL = 'http://127.0.0.1:5000/oauth/redirect'

USER_AUTH_URL = 'https://bgm.tv/oauth/authorize?' + url_parse.urlencode({
    'client_id': APP_ID,
    'response_type': 'code',
    'redirect_uri': CALLBACK_URL,
})

base_dir = pathlib.Path(path.dirname(__file__))

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def index():
    return redirect(USER_AUTH_URL)

'''
@app.route('/oauth/redirect')
def oauth_callback():
    code = request.args.get('code')
    print(code)
    resp = requests.post(
        'https://bgm.tv/oauth/access_token',
        data={
            'code': code,
            'client_id': APP_ID,
            'grant_type': 'authorization_code',
            'redirect_uri': CALLBACK_URL,
            'client_secret': APP_SECRET,
        }
    )
    try:
        r = resp.json()
        return jsonify(r)
        if 'error' in r:
            return jsonify(r)
    except json.decoder.JSONDecodeError:
        return 'error'
    return jsonify(r)
'''

'''@app.route('/oauth/redirect')
def oauth_callback():
    code = request.args.get('code')
    print(code)
    
    url = "https://bgm.tv/oauth/access_token"
    data = {
"grant_type":"authorization_code",
"client_id":"bgm22106232fa6225d8a",
"client_secret":"7402491845d1b66ce1360c33293b472a",
"code":"d155a5d3e278033b32c9d5e3f60c0499ed1bc862",
"redirect_uri":"http://127.0.0.1:5000/oauth/redirect" 
}
    response = requests.post(url, data=data)
    print(response.content.decode())
    return 'ok'
    '''
'''
@app.route('/oauth/redirect')
def oauth_callback():
    code = request.args.get('code')
    print(code)
    url='https://bgm.tv/oauth/access_token'
    headers = {'content-type': 'application/json'}
    data_json= {
"grant_type":"authorization_code",
"client_id":"bgm22106232fa6225d8a",
"client_secret":"7402491845d1b66ce1360c33293b472a",
"code":code,
"redirect_uri":"http://127.0.0.1:5000/oauth/redirect" 
}
    res =requests.post(url=url, data=json.dumps(data_json),headers = headers)
    simWords = res.json()
    #print(simWords)
    return 'ok'
    '''

@app.route('/oauth/redirect')
def oauth_callback():
    code = request.args.get('code')
    conn = http.client.HTTPSConnection("bgm.tv")
    payload = json.dumps({
      "grant_type": "authorization_code",
      "client_id": "bgm22106232fa6225d8a",
      "client_secret": "7402491845d1b66ce1360c33293b472a",
      "code": code,
      "redirect_uri": "http://127.0.0.1:5000/oauth/redirect"
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'chii_sec_id=O42uIqoA4WwTds0aDtt4UXbic3GrzTcsu8vIDhm9; chii_sid=1OoXmD'
    }
    conn.request("POST", "/oauth/access_token", payload, headers)
    res = conn.getresponse()
    raw_data = res.read()
    encoding = res.info().get_content_charset('utf8')
    data = json.loads(raw_data.decode(encoding))
    access_token=data['access_token']
    user_id=str(data['user_id'])
    print('access_token:'+access_token)
    print('user_id:'+user_id)
    return 'ok'



'''{"access_token":"a1bb3d420a2e26b45a4b3a6f4a29bdf8b0a1be62",
"expires_in":604800,
"token_type":"Bearer",
"scope":null,
"user_id":675222,
"refresh_token":"4ada3f2f286c95f02d5a6db2826b157427b737c5"
}'''

if __name__ == '__main__':
    app.run(debug=True) 


    '''{"access_token":"62d6d28cb07bd85fb6d7174d58670e66a442c5c1","expires_in":604800,"token_type":"Bearer","scope":null,"user_id":676347,"refresh_token":"ebb6b246b3940c7d138e29d23ddaec386c8ad24d"}'''