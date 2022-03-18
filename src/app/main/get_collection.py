import http.client
import json

'''
example
username="676347"
access_token="62d6d28cb07bd85fb6d7174d58670e66a442c5c1"
'''
'''{"access_token":"a1bb3d420a2e26b45a4b3a6f4a29bdf8b0a1be62",
"expires_in":604800,
"token_type":"Bearer",
"scope":null,
"user_id":675222,
"refresh_token":"4ada3f2f286c95f02d5a6db2826b157427b737c5"
}'''

'''
https://api.bgm.tv/v0/users/675222/collections
{
  "username":"675222"
}
'''

'''
{'data': [
  {'updated_at': '2022-03-18T06: 05: 09Z', 'comment': '', 'tags': [], 'subject_id': 2907, 'ep_status': 0, 'vol_status': 0, 'subject_type': 2, 'type': 1（想看）, 'rate': 0（评分）, 'private': False
  },
  {'updated_at': '2022-03-17T14: 07: 51Z', 'comment': None, 'tags': [], 'subject_id': 285666, 'ep_status': 0, 'vol_status': 0, 'subject_type': 2, 'type': 3(在看), 'rate': 8, 'private': False
  },
  {'updated_at': '2022-03-17T14: 07: 23Z', 'comment': None, 'tags': [], 'subject_id': 839, 'ep_status': 0, 'vol_status': 0, 'subject_type': 2, 'type': 2（看过）, 'rate': 9, 'private': False
  },
  },
  {'updated_at': '2022-03-12T02: 58: 48Z', 'comment': None, 'tags': [], 'subject_id': 281305, 'ep_status': 0, 'vol_status': 0, 'subject_type': 2, 'type': 2, 'rate': 8, 'private': False
  }
    ], 'total': 5, 'limit': 30, 'offset': 0
}
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

'''{
    "date": "1998-02-28",
    "platform": "剧场版",
    "images": {
        "small": "https://lain.bgm.tv/pic/cover/s/8f/7d/839_0uIrU.jpg",
        "grid": "https://lain.bgm.tv/pic/cover/g/8f/7d/839_0uIrU.jpg",
        "large": "https://lain.bgm.tv/pic/cover/l/8f/7d/839_0uIrU.jpg",
        "medium": "https://lain.bgm.tv/pic/cover/m/8f/7d/839_0uIrU.jpg",
        "common": "https://lain.bgm.tv/pic/cover/c/8f/7d/839_0uIrU.jpg"
    },
    "summary": "雾越未麻是流行音乐偶像团体“CHAM!”中的成员之一，但是在公司的决策下，她开始转型为演员。但她却感觉内心有个声音在拒绝自己的选择，而未麻的一些歌迷也反对这个决定。随着越来越多电视剧的演出，未麻却觉得自己的头脑越来越奇怪，仿佛有“另一个自己”正在形成。这时，她身边的工作人员竟一个个接连被杀。在面对社会压力和疑云之际，未麻感到越来越混乱…",
    "name": "PERFECT BLUE",
    "name_cn": "蓝色恐惧",
    "tags": [
        {
            "name": "今敏",
            "count": 2039
        },
        {
            "name": "MADHouse",
            "count": 1118
        },
        {
            "name": "剧场版",
            "count": 1054
        },
        {
            "name": "未麻的部屋",
            "count": 571
        },
        {
            "name": "1998",
            "count": 558
        },
        {
            "name": "虚实交错",
            "count": 466
        },
        {
            "name": "惊悚",
            "count": 424
        },
        {
            "name": "心理",
            "count": 419
        },
        {
            "name": "原创",
            "count": 273
        },
        {
            "name": "梦",
            "count": 263
        },
        {
            "name": "悬疑",
            "count": 211
        },
        {
            "name": "神作",
            "count": 194
        },
        {
            "name": "内涵",
            "count": 190
        },
        {
            "name": "90年代",
            "count": 76
        },
        {
            "name": "映画",
            "count": 59
        },
        {
            "name": "动画电影",
            "count": 50
        },
        {
            "name": "补旧番",
            "count": 28
        },
        {
            "name": "小说改",
            "count": 21
        },
        {
            "name": "1998年",
            "count": 19
        },
        {
            "name": "村井さだゆき",
            "count": 17
        },
        {
            "name": "日本",
            "count": 15
        },
        {
            "name": "松尾衡",
            "count": 14
        },
        {
            "name": "动画",
            "count": 13
        },
        {
            "name": "电影",
            "count": 13
        },
        {
            "name": "日本动画",
            "count": 10
        },
        {
            "name": "村井贞之",
            "count": 10
        },
        {
            "name": "1990s",
            "count": 9
        },
        {
            "name": "偶像",
            "count": 9
        },
        {
            "name": "劇場版",
            "count": 9
        },
        {
            "name": "经典",
            "count": 9
        }
    ],
    "infobox": [
        {
            "key": "中文名",
            "value": "蓝色恐惧"
        },
        {
            "key": "别名",
            "value": [
                {
                    "v": "未麻的房间"
                },
                {
                    "v": "パーフェクトブルー"
                },
                {
                    "v": "未麻的部屋"
                }
            ]
        },
        {
            "key": "上映年度",
            "value": "1998年2月28日"
        },
        {
            "key": "片长",
            "value": "81 min"
        },
        {
            "key": "原作",
            "value": "竹内義和"
        },
        {
            "key": "导演",
            "value": "今敏"
        },
        {
            "key": "演出",
            "value": "松尾衡"
        },
        {
            "key": "色彩设计",
            "value": "橋本賢"
        },
        {
            "key": "摄影监督",
            "value": "白井久男"
        },
        {
            "key": "音乐",
            "value": "幾見雅博"
        },
        {
            "key": "音响监督",
            "value": "三間雅文"
        },
        {
            "key": "话数",
            "value": "1"
        }
    ],
    "rating": {
        "rank": 18,
        "total": 4772,
        "count": {
            "1": 7,
            "2": 5,
            "3": 5,
            "4": 6,
            "5": 31,
            "6": 71,
            "7": 358,
            "8": 1259,
            "9": 1972,
            "10": 1058
        },
        "score": 8.7
    },
    "total_episodes": 1,
    "collection": {
        "on_hold": 120,
        "dropped": 36,
        "wish": 1850,
        "collect": 6554,
        "doing": 78
    },
    "id": 839,
    "eps": 1,
    "volumes": 0,
    "locked": false,
    "nsfw": false,
    "type": 2
}'''

def get_anime_name(subject_id):
      conn = http.client.HTTPSConnection("api.bgm.tv")
      payload = json.dumps({
        "subject_id": subject_id
      })
      headers = {
        'Content-Type': 'application/json',
        'Cookie': 'chii_sec_id=O42uIqoA4WwTds0aDtt4UXbic3GrzTcsu8vIDhm9; chii_sid=tkJLIg; chii_sid=6At8A5'
      }
      conn.request("GET", "/v0/subjects/%s"%subject_id, payload, headers)
      res = conn.getresponse()
      raw_data = res.read()
      encoding = res.info().get_content_charset('utf8')
      data = json.loads(raw_data.decode(encoding))
      return data['name_cn']

def switch_type(type):
      if type==1:
            return '想看'
      if type==2:
            return '看过'
      if type==3:
            return '在看'
      if type==4:
            return '搁置'
      if type==1:
            return '抛弃'


if __name__=="__main__":
      data=get_collections("62d6d28cb07bd85fb6d7174d58670e66a442c5c1")
      datalist=data['data']
      for item in datalist:
            print(get_anime_name(item['subject_id']))
            print(switch_type(item['type']))
            print(item['rate'])
            print(item['comment'])
            pass

