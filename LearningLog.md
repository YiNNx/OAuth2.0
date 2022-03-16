# Learning Log

#### day 0___3.11

- 确定选题OAuth2.0
- Github 初始化 Repository 、创建learninglog & 思考下框架 & 搞定git

#### day 1___3.12

> - [x] ~~加入Bangumi并被安利双城之战~~
>
> - [x] 学习Flask框架的使用
>
>   [Flask中文文档](https://dormousehole.readthedocs.io/en/1.1.2/quickstart.html)
>
>   [Flask 基础篇](https://zhuanlan.zhihu.com/p/44859752)
>
>   [使用 Flask 开发 Web 应用（一）](https://segmentfault.com/a/1190000008404692)
>
> - [x] 学习如何实现API
>
>   [用Python 的Flask实现 RESTful API(学习篇)](https://www.jianshu.com/p/33160c224732)
>
> - [ ] 系统学一下MySQL
>
>   [廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1177760294764384)
>

今天大部分的时间都花在了学习Flask框架和API开发上面。之前从来没接触过API这个概念，也从没仔细思考过前后端应该通过什么样的方式分离。因此尝试了解API之后感觉打开了新世界的大门。但刚开始上手写时还是毫无头绪T T。之前写的iFleaBooks那个小项目里虽然也涉及用户的注册登录什么的，但都运行在本地命令行，逻辑非常之简单，控制输入输出就行了。而API中使用web请求和响应实现数据传输与处理，如何通过Flask实现这一过程还是感觉有点没完全掌握。

话说刚开始上手写的时候翻来覆去de一些简单的bug真的好折磨人...不过实现了最基础的表单注册，看着数据成功储存进User类还是蛮开心的。

下午和晚上都有些事儿耽搁了不少时间，再加上一开始对API开发的不熟悉，感觉进度有点慢了T T。希望明天能把数据库和输入条件约束啥的搞完，顺利完成阶段一。

#### day 2___3.13

> - [x] 继续学Flask，把官方文档看完
> - [x] 看完MySQL
> - [ ] 完成注册登录的SQLAlchemy部分
> - [x] 完成注册登录的错误输入处理
> - [ ] 琢磨一下邮箱验证

学了一上午数据库，尝试使用Python进行数据库操作的过程也还算顺利，也没有出现什么令人崩溃的bug。感动！

继续进行SQLALchemy的操作。

#### day 3___3.14

> - [x] SQLAlchemy完成
>
> - [x] 了解 [OAuth2.0](https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html) 机制 & 具体过程

被bug按在地上反复摩擦的一天......anyway上午把阶段一粗糙地完成了。为什么阶段一感觉起来很简单但写起来还是超难。进度很显然太慢了。开始研究OAuth2.0。

不过值得一提的是成功实现了科学上网！在StackOverflow上查到了好几个bug的解决方法，以及google到了code和token的生成原理，真的很好用了。

#### day 4__3.15

> - [x] OAuth2.0 第三⽅⽹站注册
> - [x] OAuth2.0 处理 Client ID 和 回调链接，redirect并返回 code 
> - [x] OAuth2.0 处理 Client ID 、 Client secrets 和 code，向第三⽅⽹站提供对应⽤⼾的 token

在逻辑上完成了OAuth2.0第二阶段部分。

#### day 5__3.16

> - [x] OAuth2.0 调试
> - [x] 番剧查看和收藏功能
> - [ ] 搜索收藏的番剧

有一种熬过黑暗迎来黎明的感觉。OAuth2.0实在太难写了，昨天写得整个人丧心病狂丧失希望，但还是坚持捋顺逻辑写了下去。今天调试出来好像流程都能对上，感动。

第三阶段部分相比之下就简单快乐很之多，下午加晚上除了搜索部分，其他基本功能都完成差不多了。

#### day 6__3.17

> - [ ] 完成第三阶段
> - [ ] 添加注册的邮箱验证功能
> - [ ] 改一下第一阶段的api
> - [ ] 尝试第四阶段

#### day 7___3.18

