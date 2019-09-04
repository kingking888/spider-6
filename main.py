# -*- coding:utf-8 -*-
#-引入依赖

from consumer.server.server.systems.Fetch   import Fetch
from consumer.server.server.systems.DBase   import DBase
from consumer.server.server.systems.Mongo   import Mongo
from consumer.server.server.services.Funny  import Funny

"""
加载数据库配置文件
"""

fetch  = Fetch()
dbase  = DBase(fetch.load('./consumer/server/server/config/mysql.json'))
mongo  = Mongo(fetch.load('./consumer/server/server/config/mongo.json'))
funny  = fetch.load('./consumer/server/server/config/funny.json')

"""
更新标签文件
"""
funny = Funny(funny,dbase,mongo)

"""
抓取标签文件
"""
funny.getTagList(1)

"""
抓取视频内容
"""
funny.getTagVideoList(1,2)




