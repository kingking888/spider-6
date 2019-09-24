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
def updateQiniu():
    data = funny.getVideoList(1)
    if len(data) <= 0 : return True
    for item in  data:
        try:
            # .上传视频
            result = Qiniu.fetchFile(item['video_id'], 'https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fb10000bgbqlj481ukql40elu5g&line=0&ratio=720p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate=0&iid=35628056608&device_id=46166618999&os_api=18&app_name=aweme&channel=App%20Store&idfa=00000000-0000-0000-0000-000000000000&device_platform=iphone&build_number=27014&vid=2ED380A7-F09C-6C9E-90F5-862D58F3129C&openudid=21dae85eeac1da35a69e2a0ffeaeef61c78a2e98&device_type=iPhone8%2C2&app_version=2.7.0&version_code=2.7.0&os_version=12.0&screen_width=1242&aid=1128&ac=WIFI')
            print(result)
            if result['fsize'] > 0:
                funny.updateVideo(item['id'], {
                    'grad_time': int(time.time()),
                    'video_url': 'http://' + config['resDomain'] + '/' + result['key'],
                    'video_size': result['fsize'],
                    'cover_pic':'http://' + config['resDomain'] + '/' + result['key'] + '?vframe/jpg/offset/1'
                })
            print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE VIDEO ID:" + str(item['id']))
        except:
            print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE ERROR ID:" + str(item['id']))
            continue
        finally:
            pass
        updateQiniu()

"""
上传视频文件 | 递归上传文件
"""
#-- updateQiniu()

def updateMongo():
    data = funny.getVideoList(1000)
    if len(data) <= 0 : return True
    for item in  data:
        try:
                funny.updateVideo(item['id'], {
                    'id': ObjectId(),
                })
                print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE VIDEO ID:" + str(
                    item['id']))
        except:
            print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] UPDATE ERROR ID:" + str(item['id']))
            continue
        finally:
            pass
    updateMongo()

updateMongo()






