# -*- coding:utf-8 -*-
#-引入依赖
from systems.Fetch import Fetch
from daos.VideoDao import VideoDao
from daos.TagDao import TagDao
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
            print urix
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