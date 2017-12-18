# -*- coding:utf-8 -*-
#-引入依赖
import requests
from lxml import etree
from urllib import unquote
import time
import datetime
import random
import json
from DBaseClass import DBase
from KeepClass import Keep
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#.获取Keep对象
keep =Keep('xiaomamaster','jeepsql@123','rm-2ze201b8id2f86eoro.mysql.rds.aliyuncs.com','jeepadmin')
spider = keep.load("spider.json")
#.循环爬取数据
for x in spider['ids']:
    status=keep.mainx(spider['linkUri'].replace('@tabId', str(x)), spider['xpath'], spider['checkUri'], spider['articleTable'], spider['table'], spider['type'], spider['nature'],spider['jsStr'])
    if status==2 : continue
#.执行数据库回掉
keep.getContents('https://api.xiaomatv.cn/Action/startProcedure',2,'')