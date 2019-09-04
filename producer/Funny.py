# -*- coding:utf-8 -*-
#-引入依赖
from systems.Fetch import Fetch
import time
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
    def __init__(self,config = None,db = None,mo = None) :
        self.tagList        = config['tagList']
        self.tagVideoList   = config['tagVideoList']
        self.tagCommentList = config['tagCommentList']
        self.TagDao         = TagDao(db,mo)
        self.VideoDao       = VideoDao(db,mo)
        self.tagFiexdPath   = config['tagFiexd']['basePath']
        self.tagFiexdJson   = config['tagFiexd']['fiexd']

    """
    # 获取标签方法
    """
    def getTagList(self,page = 100):
        for i in range(0,page):
            urix = self.tagList.replace('@PageNum',str(i))
            data = Fetch().getAPI(urix,'json')
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
    def getTagVideoList(self,page = 100):
        data = self.TagDao.select('id ASC',1,10000)
        for item in data :
            print item['hash']
            for i in range(0, page):
                urix = self.tagVideoList.replace('@PageNum', str(i)).replace('@TagId', str(item['hash']))
                links = Fetch().getAPI(urix, 'json')
                for x in links['data']['data'] :
                    if x['item']['video'] == None :
                        print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']  IS NOT VIDEO'
                        continue
                    fiexd = {}
                    fiexd['title']              = x['item']['video']['text']
                    fiexd['tag_id']             = item['id']
                    fiexd['cover_pic']          = x['item']['video']['cover_image']['url_list'][0]['url']
                    fiexd['video_url']          = x['item']['video']['video_high']['url_list'][0]['url']
                    fiexd['description']        = ''
                    fiexd['user_nickname']      = x['item']['author']['name']
                    fiexd['user_pic']           = x['item']['author']['avatar']['download_list'][0]['url']
                    fiexd['user_desc']          = x['item']['author']['description']
                    fiexd['hash']               = x['cell_id']
                    fiexd['video_id']           = x['item']['video']['video_id']
                    fiexd['height']             = x['item']['video']['video_high']['height']
                    fiexd['width']              = x['item']['video']['video_high']['width']
                    fiexd['size']               = 0
                    fiexd['duration']           = x['item']['video']['duration']
                    self.VideoDao.insert(1,1,fiexd)
    """
        获取视频数据
    """
    def getVideoList(self,pageSize = 1000):
        return self.VideoDao.select('id ASC',1,pageSize)

    """
        修改视频数据
    """
    def updateVideo(self,id,data):
        self.VideoDao.update(id,data)

