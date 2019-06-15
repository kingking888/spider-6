# -*- coding:utf-8 -*-
#-引入依赖
"""
from  systems.DBase  import DBase
from  systems.Single import Singleton
from  systems.Mongo  import Mongo
from

"""
from systems.Fetch import Fetch
from systems.DBase import DBase
from systems.Mongo import Mongo
from daos.ArticleDao import ArticleDao

"""
加载数据库配置文件
"""

dbase = DBase(Fetch().load('./config/mysql.json'))
mongo = Mongo(Fetch().load('./config/mongo.json'))

print ArticleDao(dbase,mongo).check('xxxxx')