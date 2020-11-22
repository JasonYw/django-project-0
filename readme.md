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
            