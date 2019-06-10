# -*- coding:utf-8 -*-
#-引入依赖
"""
from  core.DBase  import DBase
from  core.Single import Singleton
from  core.Mongo  import Mongo

"""
from core.Query import Query;
import requests;
from lxml import etree
x = Query()
y = Query()
print  x
print  y
contents = x.getHTML('https://blog.csdn.net/zxcbnmlei/article/details/17924445')
print contents