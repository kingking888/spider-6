# -*- coding:utf-8 -*-
# -引入依赖
import time
import datetime
from models.VideoModel import VideoModel
from BaseDao import BaseDao
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
    # 方法: VideoDao video
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
            if (self.check(fiexd['hash'])) :
                print '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']  EXISTS A VIDEO'
                return 0
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
            video.video_duration= fiexd['duration']
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
    # 方法: VideoDao check
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
        """./../server/sqls/checkHash.sql"""
        return self.checkHash(self.db,self.check.__doc__,VideoModel(),hash)

    """
    #####################################################
    # 方法: VideoDao select
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
    def select(self,order = 'create_time ASC',pageNum = 1,pageSize = 20):
        """./../server/sqls/selectVideo.sql"""
        data = self.selectTable(
            self.db, self.select.__doc__, order,(pageNum - 1)*pageSize,pageSize
        )
        result = []
        for x in data : result.append(
            VideoModel(x).arrayModel.copy()
        )
        return result
    """
    #####################################################
    # 方法: VideoDao : update
    # ---------------------------------------------------
    # 描述: 更新数据
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
    def update(self,id,data):
        return  self.save(VideoModel,id,data)
    """
    #####################################################
    # 方法: VideoDao recommend
    # ---------------------------------------------------
    # 描述: 视频推荐
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
    def recommend(self,order = 'ASC',pageNum = 1,pageSize = 20):
        """/home/spider/consumer/server/server/sqls/selectRecommend.sql"""
        data = self.selectTable(
            self.db, self.recommend.__doc__, order,(pageNum - 1)*pageSize,pageSize
        )
        result = []
        for x in data : result.append(
            VideoModel(x).arrayModel.copy()
        )
        return result

