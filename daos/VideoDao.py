# -*- coding:utf-8 -*-
# -引入依赖
import hashlib
import time
import datetime
from urllib import unquote
from models.VideoModel import VideoModel
from daos.BaseDao import BaseDao
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：学习使人进步，骄傲使人落后
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""
class VideoDao(BaseDao):

    pass

    """
    # 初始化方法
    """
    def __init__(self, DBase = None,Mongo = None):
        super(VideoDao, self).__init__(DBase, Mongo)
    """
    #####################################################
    # 方法: TagDao : video
    # ---------------------------------------------------
    # 描述: 保存视频信息
    # ---------------------------------------------------
    # 参数:
    # param:in--   Object : object  : 方法参数
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def insert(self,type,nature,fiexd):
        try:
            if (self.check(fiexd['hash'])): return 0
            video = VideoModel()
            video.title         = fiexd['title']
            video.tag_id        = fiexd['tag_id']
            video.cover_pic     = fiexd['cover_pic']
            video.video_url     = fiexd['video_url']
            video.description   = fiexd['description']
            video.user_nickname = fiexd['user_nickname']
            video.user_pic      = fiexd['user_pic']
            video.user_desc     = fiexd['user_desc']
            video.hash          = fiexd['hash']
            video.video_id      = fiexd['video_id']
            video.height        = fiexd['height']
            video.width         = fiexd['width']
            video.size          = fiexd['size']
            video.duration      = fiexd['duration']
            video.type          = type
            video.nature        = nature
            video.status        = 5
            video.create_time   = int(time.time())
            video.modify_time   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            video.operator      = "SYSTEM"
            video.version       = 1
            video.remark        = ''
            return self.add(video)
        except Exception,e:
            return None
        finally:
            pass

    """
    #####################################################
    # 方法: TagDao : check
    # ---------------------------------------------------
    # 描述: 检测是否存在
    # ---------------------------------------------------
    # 参数:
    # param:in--   Object : object  : 方法参数
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def check(self,hash):
        """./sqls/checkHash.sql"""
        return self.checkHash(self.db,self.check.__doc__,VideoModel(),hash)
