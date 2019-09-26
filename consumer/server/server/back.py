# -*- coding:utf-8 -*-
#-引入依赖
import time
import datetime
from systems.Fetch import Fetch
from systems.DBase import DBase
from systems.Mongo import Mongo
from services.Funny import Funny
from librarys.QiniuYun import QiniuYun
from bson import ObjectId

"""
加载数据库配置文件
"""
fetch  = Fetch()
dbase  = DBase(fetch.load('./config/mysql.json'))
mongo  = Mongo(fetch.load('./config/mongo.json'))
funny  = fetch.load('./config/funny.json')
config = fetch.load('./config/qiniu.json')
Qiniu  = QiniuYun(config)

"""
获取抓取对象
"""
funny = Funny(funny,dbase,mongo,fetch,Qiniu,config)


"""
上传视频文件 | 递归上传文件
"""

def updateMongo():
    data = dbase.SELECT("SELECT  COUNT(1) NUM,user_nickname,user_pic,CONCAT('user_pic_image_',`hash`) "
                        "FROM    t_video "
                        "WHERE   INSTR(user_pic,'https:') > 0 "
                        "GROUP   BY user_nickname ORDER BY NUM DESC LIMIT 0,1000"
    );
    for x in data :
        result = Qiniu.fetchFile(x[3],x[2])
        if result != None and result['fsize'] > 0 :
            dbase.UPDATE('t_video',{'user_nickname':x[1]},{'user_pic':x[3]})
            print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE VIDEO UN:" + x[1])
updateMongo()






