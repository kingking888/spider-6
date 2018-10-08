# -*- coding:utf-8 -*-
#-引入依赖
"""
from  core.DBase  import DBase
from  core.Single import Singleton
from  core.Mongo  import Mongo

"""
from  production.Find  import Find

x = Find()
y = x.load('config/spider.json')
x.startWork(y[2])