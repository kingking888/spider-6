# -*- coding:utf-8 -*-
# -引入依赖
import hashlib
import time
import datetime
from urllib import unquote
from models.TagModel import TagModel
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：学习使人进步，骄傲使人落后
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""
class BaseDao(object):

    pass

    """
    # 初始化方法
    """
    def __init__(self, DBase = None,Mongo = None):
        self.db = DBase
        self.mo = Mongo

    """
    #####################################################
    # 方法: Base : checkHash
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
    def checkHash(self,DB = None,SQL = '',Model = None,hash = ''):
        try:
            if type(hash) == int : hash = str(hash)
            with open(SQL) as file :
                sql = str(file.read()).replace('@TABLE_NAME',Model.tableName).replace('@HASH',str(hash))
                file.close()
            count = DB.SELECT(sql)
            for x in count:
                for i in x : num = i
            if num > 0:
                return True
            else:
                return False
        except:
            return False
        finally:
            pass
    """
    #####################################################
    # 方法: BaseDao : insert
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
    def add(self,Model = None):
        try:
            return self.db.INSERT(Model.tableName, Model.get())
        except:
            return 0
        finally:
            pass
    """
    #####################################################
    # 方法: Base : selectTable
    # ---------------------------------------------------
    # 描述: 查询数据表
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
    def selectTable(self,DB = None,SQL = '',ORDER = '', START = 0, LASTD = 20):
        try:
            with open(SQL) as file :
                sql = str(file.read()).replace('@ORDER',ORDER).replace('@START',str(START)).replace('@LASTD',str(LASTD))
                file.close()
            return DB.SELECT(sql)
        except:
            return False
        finally:
            pass

    """
    #####################################################
    # 方法: BaseDao : save
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
    def save(self,Model = None,id = 0,data = {}):
        try:
            return self.db.UPDATE(Model.tableName, {'id' : id},data)
        except:
            return 0
        finally:
            pass
