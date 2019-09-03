# -*- coding:utf-8 -*-
#-引入依赖
import sys

from systems.Fetch  import Fetch
from systems.DBase  import DBase
from systems.Mongo  import Mongo
from producer.Funny import Funny

"""
加载数据库配置文件
"""

dbase = DBase(Fetch().load('./config/mysql.json'))
mongo = Mongo(Fetch().load('./config/mongo.json'))
funny = Fetch().load('./config/funny.json')

"""
更新标签文件
"""

funny = Funny(funny,dbase,mongo)

#.funny.getTagList(1)

funny.getTagVideoList(1)


"""
根据标签获取数据
"""


