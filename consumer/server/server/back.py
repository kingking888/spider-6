# -*- coding:utf-8 -*-
#-引入依赖
import time
import datetime
from systems.Fetch import Fetch
from systems.DBase import DBase
from systems.Mongo import Mongo
from services.Funny import Funny
from librarys.QiniuYun import QiniuYun

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
funny = Funny(funny,dbase,mongo,fetch)


"""
上传视频文件 | 递归上传文件
"""
def updateQiniu():
    data = funny.getVideoList(1)
    if len(data) <= 0 : return True
    for item in  data:
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
        updateQiniu()

"""
上传视频文件 | 递归上传文件
"""
updateQiniu()






