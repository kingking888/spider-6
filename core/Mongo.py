# -*- coding:utf-8 -*-

import pymongo

from Single import Singleton

"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫数据库基础操作类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
"""

class Mongo(Singleton):
    #.定义只读对象
    dbRead  = object
    #.定义只写对象
    dbWrite = object
    """
    #####################################################
    # 方法:: Mongo ::__init__
    # ---------------------------------------------------
    # 描述:: 数据库类初始化方法
    # ---------------------------------------------------
    # 参数:
    # param1:in--   String : readLink  :: 只读连接
    # param2:in--   String : writeLink :: 只写连接
    # ---------------------------------------------------
    # 返回：
    # return:out--  无
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def __init__(self,config = {}) :
        self.dbRead  = pymongo.MongoClient(config['readLink'])
        self.dbWrite = pymongo.MongoClient(config['writeLink'])
    """
    #####################################################
    # 方法:: Mongo :: SELECTONE
    # --------------------------------------------------
    # 描述:: 数据库查询方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Map    : where      :: 条件
    # param4:in--   Map    : order      :: 排序
    # param5:in--   Map    : limit      :: 截取
    # param6:in--   Map    : fixed      :: 字段
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def SELECTONE(self,dataName,tableName,where,order,limit,fixed) :
        try:
            mongo  = self.dbRead[dataName][tableName]
            result = mongo.find_one(where,fixed).sort(order).skip(limit[0]).limit(limit[1])
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: SELECTALL
    # --------------------------------------------------
    # 描述:: 数据库修改方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Map    : where      :: 条件
    # param4:in--   Map    : order      :: 排序
    # param5:in--   Map    : limit      :: 截取
    # param6:in--   Map    : fixed      :: 字段
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def SELECTALL(self,dataName,tableName,where,order,limit,fixed):
        try:
            mongo  = self.dbRead[dataName][tableName]
            result = mongo.find(where,fixed).sort(order).skip(limit[0]).limit(limit[1])
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: INSERTONE
    # --------------------------------------------------
    # 描述:: 数据库插入方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Map    : data       :: 条件
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def INSERTONE(self,dataName,tabelName,data) :
        try:
            mongo  = self.dbWrite[dataName][tabelName]
            result = mongo.insert(data)
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: INSERTALL
    # --------------------------------------------------
    # 描述:: 数据库插入方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Array  : data       :: 条件
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def INSERTALL(self,dataName,tabelName,data):
        try:
            mongo  = self.dbWrite[dataName][tabelName]
            result = mongo.insert_many(data)
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: UPDATEONE
    # --------------------------------------------------
    # 描述:: 数据库更新方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Array  : where      :: 条件
    # param4:in--   Map    : data       :: 数据
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def UPDATEONE(self,dataName,tableName,where,data) :
        try:
            mongo  = self.dbWrite[dataName][tableName]
            result = mongo.update_one(where,data)
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: UPDATEALL
    # --------------------------------------------------
    # 描述:: 数据库修改方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Array  : where      :: 条件
    # param4:in--   Map    : data       :: 数据
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def UPDATEALL(self,dataName,tableName,where,data) :
        try:
            mongo  = self.dbWrite[dataName][tableName]
            result = mongo.update_many(where,data)
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: DELETEONE
    # --------------------------------------------------
    # 描述:: 数据库删除方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tabelName  :: 表名
    # param3:in--   Map    : data       :: 条件
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def DELETEONE(self,dataName,tableName,where) :
        try:
            mongo  = self.dbWrite[dataName][tableName]
            result = mongo.delete_one(where)
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: DELETEALL
    # --------------------------------------------------
    # 描述:: 数据库删除方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tableName  :: 表名
    # param3:in--   Map    : where      :: 条件
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def DELETEALL(self,dataName,tableName,where) :
        try:
            mongo  = self.dbWrite[dataName][tableName]
            result = mongo.delete_many(where)
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: DELETEALL
    # --------------------------------------------------
    # 描述:: 数据库删除方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tableName  :: 表名
    # param3:in--   Map    : where      :: 条件
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def COUNT(self,dataName,tableName,where) :
        try:
            mongo  = self.dbRead[dataName][tableName]
            result = mongo.find(where).count()
            return result
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Mongo :: DELETEALL
    # --------------------------------------------------
    # 描述:: 数据库删除方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : dataName   :: 库名
    # param2:in--   String : tableName  :: 表名
    # param3:in--   Map    : where      :: 条件
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def DROP(self,dataName,tableName) :
        try:
            mongo  = self.dbWrite[dataName][tableName]
            result = mongo.drop()
            return result
        except Exception, e:
            return None
        finally:
            pass