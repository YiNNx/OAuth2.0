

> A Bingyan Internship task. Good luck to me.

# bangumoe的OAuth2.0服务 

提供⽤⼾注册并管理⾃⼰的基本信息的功能，同时对外提供OAuth2.0的服务。 

#### 阶段⼀

实现最基本的⽤⼾注册登录和修改信息的API。

#### 阶段⼆

实现OAuth2.0 Server。

#### 阶段三

参考bangumi，提供⼀个番剧收藏功能。 

#### 阶段四

提供绑定bangumi账号的API，在绑定之后，将bangumi的对应数据同步到对应⽤⼾的数据中。 



## OAuth2.0 Server:

1. client在`/aouth2.0/sign`注册应用，自定义密匙，获得client ID

2. 进行第三方登录时，用户跳转到授权页`/oauth2.0/show`，client向`/aouth2.0/show`传递client_id和redirect_url，同时用户在授权页登录：

   （实际上是无法用postman模拟发送client_id和redirect_url的，必须用户跳转：http://127.0.0.1:5000/oauth2.0/show?client_id=IPfapHgWOn58ycjMCRBD&redirect_url=http://127.0.0.1:5000/client/redirect 然后手动授权。）

   ```
   { 
   
   	"client_id":"IPfapHgWOn58ycjMCRBD", 
   
   	"redirect_url":"http://127.0.0.1:5000/client/redirect",
   
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

3. client获取code后，向`/aouth2.0/granttoken`发送client_id、client_secrets和code：

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

用户点击”绑定第三方bangumi账号“，跳转到bangumi授权页进行授权。

授权后client将获取的access_token写入数据库，利用bangumi提供的api导入用户番剧收藏数据。
