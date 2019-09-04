# -*- coding:utf-8 -*-
#-引入依赖
import time
import datetime
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
config = Fetch().load('./config/qiniu.json')
Qiniu = QiniuYun(config)

funny = Funny(funny,dbase,mongo)

"""
上传视频文件
"""
for item in funny.getVideoList(1000) :
    result = Qiniu.fetchFile(item['video_id'],item['video_url'])
    if result['fsize'] > 0 :
        funny.updateVideo(item['id'],{
            'grad_time'  : int(time.time()),
            'video_url'  : 'http://' + config['resDomain'] + '/' + result['key'],
            'video_size' : result['fsize']
        })
    retImg = Qiniu.fetchFile('cover_image_' + item['video_id'],item['cover_pic'])
    if retImg['fsize'] > 0 :
        funny.updateVideo(item['id'],{
            'cover_pic'  : 'http://' + config['resDomain'] + '/' + 'cover_image_' + item['video_id'] +
                           '?imageView2/1/format/png'
        })
    print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE VIDEO ID:" + str(item['id'])




