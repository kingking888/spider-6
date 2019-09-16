# -*- coding:utf-8 -*-
#-引入依赖
import time
import traceback 
import datetime
from daos.VideoDao import VideoDao
from daos.TagDao   import TagDao
class Funny(object):
    tagList        = ''
    tagVideoList   = ''
    tagCommentList = ''
    VideoDao       = object
    TagDao         = object
    tagFiexdPath   = ''
    tagFiexdJson   = {}

    """
    # 初始化方法
    """
    def __init__(self,config = None,db = None,mo = None,fe = None,qi = None,qiconf = None) :
        self.tagList        = config['tagList']
        self.tagVideoList   = config['tagVideoList']
        self.tagCommentList = config['tagCommentList']
        self.TagDao         = TagDao(db,mo)
        self.VideoDao       = VideoDao(db,mo)
        self.Fetch          = fe
        self.Qiniu          = qi
        self.QiConf         = qiconf
        self.tagFiexdPath   = config['tagFiexd']['basePath']
        self.tagFiexdJson   = config['tagFiexd']['fiexd']

    """
    # 获取标签方法
    """
    def getTagList(self,page = 100):
        for i in range(0,page):
            urix = self.tagList.replace('@PageNum',str(i))
            data = self.Fetch.getAPI(urix,'json')
            data = self.__getTagData(data)
            data = self.__getTagMap(data)
            for item in data:
                self.TagDao.insert(item)

    """
    # 获取标签列表
    """
    def __getTagData(self,data):
        for x in self.tagFiexdPath.split('/'):
            if x <> '': data = data[x]
        return data

    """
    # 获取数据详情
    """
    def __getTagMap(self,data):
        ret = []
        for item in data:
            muse = {}
            for key in self.tagFiexdJson:
                val = item
                keys = self.tagFiexdJson[key].split('/')
                if len(keys) == 1 :
                    muse.setdefault(key,self.tagFiexdJson[key])
                else:
                    for x in keys :
                        if x <> '':
                            if x.isnumeric() :
                                val = val[int(x)]
                            else:
                                val = val[str(x)]
                    muse.setdefault(key,val)
            ret.append(muse)
        return ret

    """
    # 获取标签方法
    """
    def getTagVideoList(self,start = 0,page = 100):
        data = self.TagDao.select('id ASC',1,1000)
        for item in data :
                print item['hash']
                for i in range(start,page):
                    try:
                        print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]  PAGE_NUMS:" + str(
                            item['id']) + "-" + str(i)
                        urix = self.tagVideoList.replace('@PageNum', str(i)).replace('@TagId', str(item['hash']))
                        links = self.Fetch.getAPI(urix, 'json')
                        if (links is None) : continue
                        for x in links['data']['data']:
                            if x['item']['video'] == None : continue
                            fiexd = {}
                            fiexd['title']          = x['item']['video']['text']
                            fiexd['tag_id']         = item['id']
                            fiexd['cover_pic']      = x['item']['video']['cover_image']['url_list'][0]['url']
                            fiexd['video_url']      = x['item']['video']['video_high']['url_list'][0]['url']
                            fiexd['description']    = ''
                            fiexd['user_nickname']  = x['item']['author']['name']
                            fiexd['user_pic']       = x['item']['author']['avatar']['download_list'][0]['url']
                            fiexd['user_desc']      = x['item']['author']['description']
                            fiexd['hash']           = x['cell_id']
                            fiexd['video_id']       = x['item']['video']['video_id']
                            fiexd['height']         = x['item']['video']['video_high']['height']
                            fiexd['width']          = x['item']['video']['video_high']['width']
                            fiexd['size']           = 0
                            fiexd['duration']       = x['item']['video']['duration']
                            once = self.VideoDao.insert(1, 1,fiexd)
                            if once <> 0 : self.updateQiniu(once)
                    except Exception, e:
                    	traceback.print_exc()
                        continue
                    finally:
                        pass
    """
        获取视频数据
    """
    def getVideoList(self,pageSize = 500):
        return self.VideoDao.select('id ASC',1,pageSize)

    """
        修改视频数据
    """
    def updateVideo(self,id,data):
        self.VideoDao.update(id,data)

    """
        获取推荐视频
    """
    def getRecommend(self,pageSize = 50):
        return self.VideoDao.recommend('ASC',1,pageSize)

    """
    上传视频文件 | 递归上传文件
    """

    def updateQiniu(self,item):
        try:
            # .上传视频
            result = self.Qiniu.fetchFile(item['video_id'], item['video_url'])
            if result['fsize'] > 0:
                self.updateVideo(item['id'], {
                    'grad_time': int(time.time()),
                    'video_url': 'http://' + self.QiConf['resDomain'] + '/' + result['key'],
                    'video_size': result['fsize']
                })
            # .上传封面
            retImg = self.Qiniu.fetchFile('cover_image_' + item['video_id'], item['cover_pic'])
            if retImg['fsize'] > 0:
                self.updateVideo(item['id'], {
                    'cover_pic': 'http://' + self.QiConf['resDomain'] + '/' + 'cover_image_' + item['video_id'] +
                                 '?imageView2/1/format/png'
                })
            print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]  UPDATE VIDEO ID:" + str(
                item['id'])
        except:
            print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]  UPDATE ERROR ID:" + str(
                item['id'])
        finally:
            pass


