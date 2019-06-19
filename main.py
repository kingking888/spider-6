# -*- coding:utf-8 -*-
#-引入依赖
import sys

from systems.Fetch import Fetch
from systems.DBase import DBase
from systems.Mongo import Mongo
from producer.Funny import Funny

"""
加载数据库配置文件
"""


dbase = DBase(Fetch().load('./config/mysql.json'))
mongo = Mongo(Fetch().load('./config/mongo.json'))
funny = Fetch().load('./config/funny.json')

x = Funny(funny,dbase,mongo)

data  = x.getTagList(101)
"""
# 获取执行权限
"""
role = ''
name = ''
if __name__ == '__main__':
    if len(sys.argv) == 2:
        role = sys.argv[0]
        name = sys.argv[2]
    else:
        exit(0)

"""
# 魔术倒入文件
"""
muse = __import__(role + '.' + name,fromlist = True)

"""
# 反射调用方法
"""
if hasattr(muse,'start') :
    ret = getattr(muse,'start')
    ret()
else:
    exit(0)