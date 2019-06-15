# -*- coding:utf-8 -*-
#-引入依赖
from systems.Fetch import Fetch
from producer.ProducerDao import ProducerDao
class Funny(object):
    tagList        = ''
    tagVideoList   = ''
    tagCommentList = ''
    """
    # 初始化方法
    """
    def __init__(self,config = {}) :
        self.tagList = config['tagList']
        self.tagVideoList = config['tagVideoList']
        self.tagCommentList = config['tagCommentList']
    def getTagList(self,page = 100):
        for i in range(0,page):
            data = Fetch.getAPI(self.tagList.replace('@PageNum',str(i)),'text')
