# -*- coding:utf-8 -*-
#-引入依赖
import time
import datetime
from consumer.server.server.systems.Fetch     import Fetch
from consumer.server.server.systems.DBase     import DBase
from consumer.server.server.systems.Mongo     import Mongo
from consumer.server.server.services.Funny    import Funny
from consumer.server.server.librarys.QiniuYun import QiniuYun

"""
加载数据库配置文件
"""
fetch  = Fetch()
dbase  = DBase(fetch.load('./consumer/server/server/config/mysql.json'))
mongo  = Mongo(fetch.load('./consumer/server/server/config/mongo.json'))
funny  = fetch.load('./consumer/server/server/config/funny.json')
config = fetch.load('./consumer/server/server/config/qiniu.json')
Qiniu  = QiniuYun(config)

"""
获取抓取对象
"""
funny = Funny(funny,dbase,mongo)


"""
上传视频文件
"""
for item in funny.getVideoList(1500) :
    try:
        # .上传视频
        result = Qiniu.fetchFile(item['video_id'], item['video_url'])
        if result['fsize'] > 0:
            funny.updateVideo(item['id'], {
                'grad_time': int(time.time()),
                'video_url': 'http://' + config['resDomain'] + '/' + result['key'],
                'video_size': result['fsize']
            })
        # .上传封面
        retImg = Qiniu.fetchFile('cover_image_' + item['video_id'], item['cover_pic'])
        if retImg['fsize'] > 0:
            funny.updateVideo(item['id'], {
                'cover_pic': 'http://' + config['resDomain'] + '/' + 'cover_image_' + item['video_id'] +
                             '?imageView2/1/format/png'
            })
        print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE VIDEO ID:" + str(item['id'])
    except:
        print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE ERROR ID:" + str(item['id'])
        continue
    finally:
        pass





