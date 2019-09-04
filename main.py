# -*- coding:utf-8 -*-
#-引入依赖
import sys

from systems.Fetch     import Fetch
from systems.DBase     import DBase
from systems.Mongo     import Mongo
from producer.Funny    import Funny
from librarys.QiniuYun import QiniuYun

"""
加载数据库配置文件
"""

dbase = DBase(Fetch().load('./config/mysql.json'))
mongo = Mongo(Fetch().load('./config/mongo.json'))
funny = Fetch().load('./config/funny.json')
Qiniu = QiniuYun(Fetch().load('./config/qiniu.json'))

#data = Qiniu.fetchFile('v0204cce0000bl096np1h1vsgf2p9qt0','http://v3-ppx.ixigua.com/a525b7393a2e81ee98000712a2a4d21c/5d6e4ca1/video/m/22084a0c11e287d489fa44288a78c90693f11630aeb600005844e3517f8d/?a=1319&br=1543&cr=0&cs=0&dr=6&ds=2&er=&l=20190903182039010155026014899C34&lr=&rc=M3RzaXY0NHE8bzMzaGYzM0ApZmVmZjs3ZGVlNzY4ZDY0M2dxNi9kc2VtMy1fLS1gMS9zczBfL19gLzM2L2FfYjZfYC86Yw%3D%3D')
#print data
#exit(0)

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
funny.getTagVideoList(1)




