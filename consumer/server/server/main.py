# -*- coding:utf-8 -*-
#-引入依赖
import time
from systems.Fetch     import Fetch
from systems.DBase     import DBase
from systems.Mongo     import Mongo
from services.Funny    import Funny
from librarys.QiniuYun import QiniuYun

"""
加载数据库配置文件
"""

fetch  = Fetch()
dbase  = DBase(fetch.load('./config/mysql.json'))
mongo  = Mongo(fetch.load('./config/mongo.json'))
funny  = fetch.load('./config/funny.json')
config = fetch.load('./config/qiniu.json')
Qiniu  = QiniuYun(config)

"""
获取系统时间
"""

"""
更新标签文件
"""
funny = Funny(funny,dbase,mongo,fetch,Qiniu,config)

"""
抓取标签文件
"""

funny.getTagVideoList(0,1)
