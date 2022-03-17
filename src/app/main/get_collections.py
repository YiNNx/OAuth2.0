import http.client
import json

'''
example
username="676347"
access_token="62d6d28cb07bd85fb6d7174d58670e66a442c5c1"
'''

def get_collections(access_token:str):
      user_data=get_info(access_token)
      username=user_data['username']
      conn = http.client.HTTPSConnection("api.bgm.tv")
      payload = json.dumps({
        "username": username
      })
      headers = {
        'Authorization': 'Bearer %s'%access_token,
        'Content-Type': 'application/json',
        'Cookie': 'chii_sec_id=O42uIqoA4WwTds0aDtt4UXbic3GrzTcsu8vIDhm9; chii_sid=tkJLIg; chii_sid=6At8A5'
      }
      conn.request("GET", "/v0/users/%s/collections"%username, payload, headers)
      res = conn.getresponse()
      raw_data = res.read()
      encoding = res.info().get_content_charset('utf8')
      data = json.loads(raw_data.decode(encoding))
      return data

def get_info(access_token:str,):
      '''
      info example:
      {
        "avatar":{"large":"https://lain.bgm.tv/pic/user/l/icon.jpg","medium":"https://lain.bgm.tv/pic/user/m/icon.jpg","small":"https://lain.bgm.tv/pic/user/s/icon.jpg"},
        "sign":"",
        "url":"https://bgm.tv/user/676347",
        "username":"676347",
        "nickname":"12333",
        "id":676347,
        "user_group":10
        }
      '''
      conn = http.client.HTTPSConnection("api.bgm.tv")
      payload = ''
      headers = {
        'Authorization': 'Bearer %s'%access_token,
        'Content-Type': 'application/json',
        'Cookie': 'chii_sec_id=O42uIqoA4WwTds0aDtt4UXbic3GrzTcsu8vIDhm9; chii_sid=tkJLIg; chii_sid=6At8A5'
      }
      conn.request("GET", "/v0/me", payload, headers)
      res = conn.getresponse()
      raw_data = res.read()
      encoding = res.info().get_content_charset('utf8')
      data = json.loads(raw_data.decode(encoding))
      return data

if __name__=="__main__":
      data=get_collections("62d6d28cb07bd85fb6d7174d58670e66a442c5c1")
      print(data)