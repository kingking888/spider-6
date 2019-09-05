# -*- coding:utf-8 -*-
#-引入依赖

from systems.Fetch import Fetch
from systems.DBase import DBase
from systems.Mongo import Mongo
from services.Funny import Funny

"""
加载数据库配置文件
"""

fetch  = Fetch()
dbase  = DBase(fetch.load('./config/mysql.json'))
mongo  = Mongo(fetch.load('./config/mongo.json'))
funny  = fetch.load('./config/funny.json')

"""
更新标签文件
"""
funny = Funny(funny,dbase,mongo,fetch)

"""
抓取标签文件
"""
funny.getTagList(1)

"""
抓取视频内容
"""
funny.getTagVideoList(1,1)




