# -*- coding:utf-8 -*-
# -引入依赖
import hashlib
import time
import datetime
from urllib import unquote
from models.TagModel import TagModel
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
class TagDao(BaseDao):

    pass

    """
    # 初始化方法
    """
    def __init__(self, DBase = None,Mongo = None):
        super(TagDao, self).__init__(DBase,Mongo)

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
        return self.checkHash(self.db,self.check.__doc__,TagModel(),hash)

    """
    #####################################################
    # 方法: TagDao : insert
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
    def insert(self,fiexd):
        try:
            hash = str(fiexd['hash'])
            if (self.check(hash)) : return 0
            tag             = TagModel()
            tag.title       = fiexd['title']
            tag.cover_pic   = fiexd['cover_pic']
            tag.description = fiexd['description']
            tag.hash        = hash
            tag.type        = fiexd['type']
            tag.nature      = fiexd['nature']
            tag.create_time = int(time.time())
            tag.modify_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tag.operator    = "SYSTEM"
            tag.status      = 5
            tag.remark      = ''
            return self.add(tag)
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法: TagDao : select
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
    def select(self,order = 'create_time DESC',pageNum = 1,pageSize = 20):
        """./sqls/selectTag.sql"""
        data = self.selectTable(
            self.db, self.select.__doc__, order,(pageNum - 1)*pageSize,pageSize
        )
        result = []
        for x in data : result.append(
            TagModel(x).arrayModel
        )
        return result