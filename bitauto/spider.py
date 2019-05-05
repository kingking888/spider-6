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

keep =Keep('root','root','47.95.36.78','jeepadmin')
spider = keep.load("spider.json")
"""
for x in spider:
    status=keep.mainx(x['linkUri'], x['xpath'], x['checkUri'], x['articleTable'], x['table'], x['type'],x['nature'])
    if status==2 : continue
"""