saas 平台
bug&任务追踪管理
涉及到的知识点
    虚拟环境 电脑上创建多个python环境
        django 1.11版本 -> CRM版本 -> [维护]
        django 2.0版本 ->路飞 [新开发]
    虚拟环境
        自己电脑上有一个 Py3 (django/pymysql/sms/redis/celery)
        -虚拟环境1:py3 纯净的 django 1.11
        -虚拟环境2:py3 纯净的 django 2.0
    local_settings.py 本地配置
        开发：
            连接数据库需要在django的settings  中去设置 连接数据库IP: 1.1.1.1
        测试：
            修改配置 连接数据库 1.1.1.2
        本地配置：
            在setting文件中最后一行 加入以下代码：
                try：
                    from .local_settings import *
                except:
                    pass
            在local_settings.py中做本地的配置
            在local_settings.py中重置配置
            把local_settings中加入git ignore
        开发测试 都需要写local_settings文件，并且都需要加入git ignore
    腾讯云平台（免费）
        sms短信，申请服务
        cos对象存储，腾讯给你了一个云硬盘，项目中上传文件/查看文件/下载文件
            若文件放在服务器上，很会慢，服务器最好只处理逻辑业务，把占用带宽行为 扔给腾讯云
    redis
        mysql：
            我的电脑    别人的电脑
            pymysql  ->mysql软件 -行为：创建表(本质创建文件夹) 插入数据(写入记录) (硬盘文件操作)
            redis(模块) -> redis -行为：set name="test" 10s 在内存中建立键值对,并且设置超时间 get name 在内存中获取对应的值
        注意:一台电脑也可以
    项目开发
        一期
            做用户认证 短信验证 图片验证码 登录短信登录 用户名密码登录(django modelform组件) 3天时间
        二期
            wiki 文件 问题管理  5~7天
        三期
            支付、部署（周末linux基础）2天

day01
    今日概要
        虚拟环境 项目环境
        搭建一个项目框架:local_settings
        git相关 实战应用 代码每天都提交
        python 发送短信(腾讯sms)
    今日详细
        虚拟环境 virtualenv
            安装 pip3 install virtualenv
            安装 pip3 install virtualenvwrapper
        创建虚拟环境
            方法1：
                virtualenv 环境名称
                #创建[环境名称]文件夹，放置所有的环境
                virtualenv 环境名称 --python=python版本 或者 --python=python解释器路径
            方法2：
                mkvirtualenv
        注：
            vscode运行python时提示无法加载文件xxx\.venv\Scripts\activate.ps1
                第一步：以管理员身份运行powershell
                第二步：执行：get-ExecutionPolicy 回复Restricted，表示状态是禁止的。
                第三步：执行：set-ExecutionPolicy RemoteSigned
                第四步：选择Y，回车
            windows中没有bin目录，activate.exe在scripts中
            先激活
        生成requirements.txt文件
            pip freeze > requirements.txt
        搭建django的项目环境(虚拟环境)
        警醒：
            企业做项目开发要先建立虚拟环境
        local_settings
            在settings中最后导入local_settings
            创建自己的local_settings.py
            给别人代码时切记不要给local_settings文件
    今日作业
        搭建项目环境
        python代码实现把文件上传到腾讯对象存储
        python sms

day02
    今日概要
        腾讯发送短信
        django的modelform组件
        redis
        注册逻辑的设计
        开发
        讲解
    内容回顾
        local_settings的作用：
            本地配置信息
            -开发 负责开发
            -测试 负责测试
            -运维 负责项目上线
        .gitignore的作用
            版本控制需要忽略掉的文件 不进行commit以及push
        虚拟环境的作用
            项目之间的隔离
            开发：本地环境，代码上线时，若一个服务器跑多个项目需要做环境隔离
            pip freeze > requirements.txt ->把当前虚拟环境中所有的模块均放到requirements.txt中
            pip install -r requirements.txt 把文件中所有的模块安装
            requirements 不要用其他的名字 潜规则
    今日详细
        腾讯发送短信
            注册
            登陆
            wiki：pythonav.com/wiki/detail/10/81/
            安装sdk
        Django的ModelForm
            自动生成标签
            表单验证
        redis基本操作
            安装redis
                windows版本的redis   port 6379 password 0125
                linux版本的redis 企业开发常用
            python操作redis的模块
                pythonav.com/wiki/detail/10/82/
    今日作业
        创建两个app
        注册页面
        通过ajax 手机号 发送到后台 csrftoken问题
            页面上加倒计时效果
            注册按钮 字段校验+手机号验证码验证
            python操作redis 使用django reddis模块
    下一步思路
        点击获取验证码
            获取手机号
            后台发送ajax请求
                手机号，以及是注册
            检验手机号是否合法，并向手机发送短信，
                验证码时效性处理 一分钟处理
                把手机号与验证码存入redis，同时给手机号发信息，redis有定时功能
day03
    今日概要
        注册
        短信密码登录
        用户名密码登录
    内容回顾
        虚拟环境 virtualenv
        pip freeze > requirements.txt
        local_settings.py
        gitignore
        短信腾讯云/阿里云短信(阅读文档、谷歌、必应、搜狗)
            API -> 访问url 并根据文档传入参数
            SDK -> 模块，开发包、基于模块完成功能
            优先看sdk 不行再看api
        redis，帮我们在内存中可以存取数据的软件(基于内存的数据库)
            1.在A主机安装redis&配置&启动
            2.连接redis
                方式一 利用redis提供的客户端
                方式二 利用相关模块
                    安装模块
                    使用模块
                        ->不推荐以下使用方式
                            import redis
                            # 连接redis
                            conn = redis.Redis(
                                host="192.168.1.18", port=6379, password="0125", encoding="utf-8"
                            )  # host为本机ip
                            # 设置键值对
                            # conn.set(
                            #     "15801367721", 9999, ex=60
                            # )  # 手机号 验证码 超时时间超时后自动清空此条数据，其中验证码为int 但是写入redis时会转成字符串，并通过encoding 转换成字节
                            # # 获取值
                            values = conn.get("15801367721")  # 没有值返回None，有值的话返回字节类型
                            print(values)
                        ->官方推荐使用连接池
                            import redis
                            # 连接redis
                            conn = redis.ConnectionPool(
                                host="192.168.1.18", port=6379, password="0125", encoding="utf-8",max_connections=1000
                            )  # host为本机ip
                            conn =redis.Redis(connection_pool=pool)
                            # 设置键值对
                            # conn.set(
                            #     "15801367721", 9999, ex=60
                            # )  # 手机号 验证码 超时时间超时后自动清空此条数据，其中验证码为int 但是写入redis时会转成字符串，并通过encoding 转换成字节
                            # # 获取值
                            values = conn.get("15801367721")  # 没有值返回None，有值的话返回字节类型
                            print(values)
                        ->django-redis
                            目的:在django中方便的使用redis
                            使用步骤
                                安装 pip install django-redis
                                在settings中配置，放在local_settings中
                                    CACHES ={
                                        "default:"{
                                            "BACKEND":"django_redis.cache.RedisCache",
                                            "LOCATION":"xxxxx", #安装reids的IP以及端口号
                                            "OPTIONS":{
                                                "CLIENT_CLASS":"django_reids.client.DefaultClient",
                                                "CONNECTION_POOL_KWARGS":{ #内部创建的连接池
                                                    "max_connections":1000,
                                                    "encoding":"utf-8"
                                                },
                                                "PASSWORD":'xxxxxxxx' #redis密码 #需要密码才需要加
                                            }
                                        }
                                    }
                                使用
                                    from django.shortcuts import HttpResponse
                                    from django_redis import get_redis_connection
                                    def index(request):
                                        conn =get_redis_connection("default") #去链接池获取default的连接池
                                        conn.set('nickname','rico',ex=10)
                                        value =conn.get('nickname')
                                        print(value)
                                        return HttpResponse('ok')
                                    项目中读写分离可能会用到两台redis
    今日详细
        1.2.1按钮绑定点击事件
        1.2.2获取手机号
        1.2.3发送ajax
        1.2.4手机号校验
            不能为空
            格式正确
            没有注册过
        1.2.5验证通过
            发送短信
            将短信保存在redis中
        1.2.6成功失败
            失败、错误信息
            成功、倒计时
                disabled属性
                    $('#btnSms').prop("disabled",true); 添加此属性表示不可操作
                    $('#btnSms').prop("disabled",false); 相当于移出此属性
                定时器
                    var obj =setInterval(function(){
                        console.log(123);
                    },1000) 开启定时器
                    clearInterval(obj) 关闭定时器
                实例
                    var time=60
                    var obj=setInterval(function(){
                        time =time-1
                        if(time<1){
                            clearInterval(obj)
                        }
                    },1000)

    今日回顾
        视图views.py ->views目录
        模板,根目录templates ->根据app注册顺序去每个app的templates中
        静态文件
        项目中多个app且想要各自模板，静态文件隔离，建议通过app名称再进行嵌套即可
        路由分发
            include
            namespace
        母版
            title
            css
            content
            js
        功能
            bootstrap导航条 去除圆角 container
            modelform生成html标签，自动id id_字段名
            发送ajax请求
                $.ajax({
                    url:'/index/',
                    type:'GET',
                    data:{},
                    dataType:"JSON",
                    success:function(res){
                        console.log(res)
                    }
                })
            form&modelform可以进行表单验证
                form = sendsmsform(request,data=request.POST) #queryset
                form = sendsmsform(request,data=request.GET) #queryset
            form&modelform 中如果想要用视图中的值(request)
                重写def __init__(request,*args,**kwargs)
                        super().__init__(*args,**kwargs)
                        self.request =request
            短信
            redis(Django-redis)
            倒计时
    今日作业
        点击注册按钮
        短信登录
        django实现图片验证码

day04
    内容回顾
        项目规则
            创建项目 静态、视图、路由
        ajax
            $.ajax({
                url:'..',
                type:'GET',
                data:{},
                dataType:'JSON',
                success:function(data){
                    console.log(data)
                }
            })
        moldeform/form使用request
            重写modelform/form的__init__方法，把想要的数据传递
        django-redis
    今日概要
        点击注册
        用户登录
            短信验证码
            手机or邮箱/密码登录
        项目管理
            创建星标
