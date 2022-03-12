> A Bingyan Internship task. Good luck to me : D

# bangumoe的OAuth2.0服务 

提供⽤⼾注册并管理⾃⼰的基本信息的功能，同时对外提供OAuth2.0的服务。 

## 阶段⼀  普通

### 基本要求 

你需要实现**最基本的⽤⼾注册登录**和**修改信息的API**。 关于这个功能，你需要考虑⽤⼀个合适的**数据库**储存数据， ⽤⼾的信息⾄少包括**⽤⼾名、密码、邮箱、昵称、头像、简介**。

接⼝的实现最好考虑使⽤你熟悉的语⾔的**⼀个后端框架**

tips：关于密码，⼀般不应该以明⽂直接保存

### 进阶内容 

你可不能让⽤⼾随意注册账号，**⽤⼾需要提供邮箱**，在注册时，你需要**给⽤⼾发邮件**，**⽤⼾点击后才能注册成功**，当然，它需要在⼀定时间后过期。 如果你还有余⼒，可以想办法限制⽤⼾请求邮件的频率。 

## 阶段⼆ ⾼级

### 基本要求 

本阶段建议你先了解OAuth2.0的过程 

基本的⽤⼾功能实现后，就可以开始做OAuth了。 在本阶段你需要模仿Github，实现⼀个可以对外提供的 OAuth2.0服务的功能。 

（对于Github的服务，可以通过OAuth2.0，达到第三⽅登录Github的⽬的。并在登录成功后，展⽰⽤⼾Github 的信息。） 

要求为：第三⽅⽹站可以在bangumoe注册OAuth2.0服务，需要提供服务名、bangumoe的主⻚链接、应⽤描述、回调链接（具体可以参考Github的OAuth2.0服务） 

注册完毕后提供 Client ID ，第三⽅⽹站的管理者需要⼿动⽣成 Client secrets⽤⼾在第三⽅⽹站跳转到bengumoe的登录界⾯时，会以json 的形式传来 Client ID 和 回调链接 ,如： 

bangumoe需要规范处理这些数据，redirect并返回code 。 

登录的API你已拥有，你还需要提供获取 token 的API以及获取⽤⼾信息的API。 

第三⽅⽹站在处理⽤⼾登录时会以 json 的形式传来Client ID 、 Client secrets 和 code ，如： 

```
{ 

"client_id":"4bce48389e6f4b6d955k", 

"redirect_url":"http: / w.xxx.com/oauth/re 

direct" 

}
```

bangumoe需要规范处理这些数据，如果合法，则向第三⽅⽹站提供对应⽤⼾的 token。 

## 阶段三 稀有

基本要求 

简单的⽤⼾信息并没有什么实际意义。为了让它看上去有点⽤，你需要参考bangumi，提供⼀个番剧收藏功能。 

番剧数据只需要包括：番剧名、话数、导演。⽤⼾可以有5种收藏类型： 

同时可以在收藏时对番剧进⾏评价，包括评分、吐槽（不需要标签） 

⽤⼾可以随时查看和搜索⾃⼰的收藏 

（私货，顺便安利⼀⼿双城之战） 

进阶内容 

⽤⼾可以添加其他⽤⼾为好友，在添加后，好友在收藏或评价番剧时，⽤⼾都能看到对应信息。

## 阶段四 史诗

### 基本要求 

但即使这样，你还是会不经反思到：“它真的有⽤吗?”，管他呢。 

经过⼀番努⼒bangumoe终于可以⽤了，bangumoe上线后⽤⼾向⼩l抱怨：爷为啥要⾃⼰把数据再保存⼀遍到你这个烂平台啊！ 

⼩l猛然发现bangumi提供了⾃⼰的api：https: /git hub.com/bangumi/api。 

为了让⼴⼤阿宅更好地追番，⼩l需要你的服务提供绑定bangumi账号的API，在绑定之后，将bangumi的对应数据同步到对应⽤⼾的数据中。 

tips:本质上核⼼功能就是做⼀个OAuth2.0的客⼾端。 

（编题者确实没有⽤过bangumi的OAuth，如果这个阶段遇到了什么奇怪的问题，建议不要死磕，告诉编题者，因为可能是真的不能实现） 
