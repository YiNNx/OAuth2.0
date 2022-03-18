> A Bingyan Internship task. Good luck to me.

# Bangumoe的OAuth2.0服务 

提供⽤⼾注册并管理⾃⼰的基本信息的功能，同时对外提供OAuth2.0的服务。 

#### 阶段⼀

实现最基本的⽤⼾注册（邮箱验证）、登录和修改信息的API。

#### 阶段⼆

实现OAuth2.0 Server。

#### 阶段三

参考bangumi，提供⼀个番剧收藏功能。 

#### 阶段四

提供绑定bangumi账号的API，在绑定之后，将bangumi的对应数据同步到对应⽤⼾的数据中。 （OAuth2.0 Client）



## OAuth2.0 Server:

1. client在`/aouth2.0/sign`注册应用，自定义密匙，获得client ID

2. 进行第三方登录时，用户跳转到授权页`http://127.0.0.1:5000/oauth2.0/show?client_id=xxxxxxxx&redirect_url=http://xxxxxx/redirect`，并登录：

   ```
   { 
   
   	"email":"2333@moe.com", 
   
   	"password":"233333" 
   
   }
   ```

   server确认信息后回调redirect_url，并返回code：

   ```
   { 
   
   	"code":
   "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0NzU3OTc2OSwiZXhwIjoxNjQ3NTgwMzY5fQ.Mw.ajuLe4SskMkCVK_aIlUIjetDoUndZ3F92rW_ud6BjRdLSniuSKum2xPrtQvQrCK1V3yVq9gBJSwGKWnYamDqQ" 
   
   }
   ```

3. client获取code后，向`/oauth2.0/granttoken`发送client_id、client_secrets和code：

   ```
   {
   
       "client_id": "IPfapHgWOn58ycjMCRBD",
       
       "client_secrets": "123456",
       
       "code": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0NzU4MDg4OCwiZXhwIjoxNjQ3NTgxNDg4fQ.Mw.dUPFfwWfPsyzijw5lGnx6VuaKlYBb21zlSycCkyFRVpjjEAGR2gQejmR7hWi_2JXjYAPmPoyBpkV4D6LuTGarg"
       
   }
   ```

   server返回用户对应的token。

   ```
   {
   
       "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0NzU4MDk0NiwiZXhwIjoxNjQ3NTg0NTQ2fQ.eyJlbWFpbCI6IjIzMzNAbW9lLmNvbSIsInVpZCI6M30.Kl_pri4sOp9ErP2yseuy-h_q4_884Qit6yEI0U4akUoDnBl4e6r3tmHVJj3MR5YQ7O7KmSEZAu_H-6VuD_nj7w"
       
   }
   ```

4. 获取用户信息的api：`/aouth2.0/getinfo`

   向`/aouth2.0/getinfo`发送token

   ```
   {
   
       "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0NzU4MDk0NiwiZXhwIjoxNjQ3NTg0NTQ2fQ.eyJlbWFpbCI6IjIzMzNAbW9lLmNvbSIsInVpZCI6M30.Kl_pri4sOp9ErP2yseuy-h_q4_884Qit6yEI0U4akUoDnBl4e6r3tmHVJj3MR5YQ7O7KmSEZAu_H-6VuD_nj7w"
       
   }
   ```

   server返回：

   ```
   {
       "avator": "https://bangumi.tv/user/675222",
       "email": "2333@moe.com",
       "intro": "here is moee",
       "nickname": "moee",
       "uname": "2333@moe.com"
   }
   ```

   

## OAuth2.0 Client:

1. 用户点击”绑定第三方bangumi账号“，跳转到bangumi授权页

   `https://bgm.tv/oauth/authorize?client_id=bgm22106232fa6225d8a&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Foauth%2Fredirect`

   进行授权。

2. 用户成功授权后Server跳转回redirect_uri（`http://127.0.0.1:5000/oauth2.0/redirect`），并返回code。

3. Client接收code，并向`https://bgm.tv/oauth/access_token`使用code换取token：

   ```
   POST https://bgm.tv/oauth/access_token
   ```

   ```
   {
         "grant_type": "authorization_code",
         "client_id": 'bgm22106232fa6225d8a',
         "client_secret": '7402491845d1b66ce1360c33293b472a',
         "code": code,
         "redirect_uri": 'http://127.0.0.1:5000/oauth/redirect'
   }
   ```

   接收到Server返回的access_token：

   ```json
   {
       "access_token":"xxxxxxxx",
       "expires_in":604800,
       "token_type":"Bearer",
       "scope":null,
       "refresh_token":"xxxxxxxx"
       "user_id" : xxxxx
   }
   ```

4. Client将获取的access_token写入数据库，利用bangumi提供的api导入用户番剧收藏数据。

   (bangumi提供的api似乎有点bug，没法正常导出番剧评论，但番剧名和状态是可以正常导出的)

## 邮箱验证：

利用Flask的**Flask-Mail**扩展向用户发送验证邮件

token使用itsdangerous的TimedJSONWebSignatureSerializer()生成，有效期为10分钟

用户点击验证链接，server接收到token进行解析，判断uid与session中的uid是否相符，相符则验证成功

## 数据库：

```
+--------------------+
| Tables_in_bangumoe |
+--------------------+
| users              |
| info               |
| oauth              |
| anime              |
| collection         |
+--------------------+
```

users：

```
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| uid          | int          | NO   | PRI | NULL    | auto_increment |
| uname        | varchar(32)  | NO   | UNI | NULL    |                |
| email        | varchar(64)  | NO   | UNI | NULL    |                |
| pword_hash   | varchar(511) | NO   | MUL | NULL    |                |
| statu        | int          | NO   |     | 0       |                |
| access_token | varchar(64)  | YES  |     | 0       |                |
+--------------+--------------+------+-----+---------+----------------+
```

oauth：

```
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| appname  | varchar(255) | NO   |     | NULL    |                |
| homeURL  | varchar(255) | NO   |     | NULL    |                |
| appDesc  | varchar(255) | NO   |     | NULL    |                |
| backURL  | varchar(255) | NO   |     | NULL    |                |
| clientID | varchar(255) | YES  |     | NULL    |                |
| secrets  | varchar(255) | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
```

anime：

```
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int         | NO   | PRI | NULL    | auto_increment |
| name     | varchar(64) | NO   |     | NULL    |                |
| episode  | int         | YES  |     | NULL    |                |
| director | varchar(64) | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
```

collection：

```
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | int          | NO   | PRI | NULL    | auto_increment |
| uid     | int          | NO   |     | NULL    |                |
| name    | varchar(64)  | NO   |     | NULL    |                |
| statu   | varchar(32)  | NO   |     | NULL    |                |
| score   | int          | YES  |     | NULL    |                |
| comment | varchar(256) | YES  |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+
```

