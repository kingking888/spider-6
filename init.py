# -*- coding:utf-8 -*-
#-引入依赖
"""
from  systems.DBase  import DBase
from  systems.Single import Singleton
from  systems.Mongo  import Mongo

"""
from systems.Query import Query;
import requests;
from lxml import etree
x = Query()
print  x
y = Query()
print  y
contents = x.getHTML('https://blog.csdn.net/zxcbnmlei/article/details/17924445')
print contents