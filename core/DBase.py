#!/usr/bin/env python
# -*- coding:utf-8 -*-
#.  引入依赖包
import requests
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import time
import datetime
import random
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')
##.全局变量
userName = 'root'
passWord = 'root'
localHost = 'localHost'
dataName = 'test'


##
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫数据库基础操作类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
##
class  DBase(type):
    #.定义链接对象
    dbConn = object
    #.定义单例模式
    base = object
    ##
    #####################################################
    # 方法:: DBase ::__init__
    # --------------------------------------------------
    # 描述:: 数据库类初始化方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : userName :: 用户名
    # param2:in--   String : passWord :: 用户密码
    # param3:in--   String : localHost :: 数据库地址
    # param4:in--   String : dataName :: 数据库名称
    # --------------------------------------------------
    # 返回：
    # return:out--  无
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def __init__(self,userName,passWord,localHost,dataName) :
        super(DBase,self).__init__(userName,passWord,localHost,dataName)
        #.初始化链接对象
        self.dbConn = MySQLdb.connect(
            user=userName,
            port=3306,
            passwd=passWord,
            host=localHost,
            db=dataName,
            charset='utf8'
        )
    ##
    #####################################################
    # 方法:: DBase ::__call__
    # --------------------------------------------------
    # 描述:: 数据库单例方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : userName :: 用户名
    # param2:in--   String : passWord :: 用户密码
    # param3:in--   String : localHost :: 数据库地址
    # param4:in--   String : dataName :: 数据库名称
    # --------------------------------------------------
    # 返回：
    # return:out--  无
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def __call__(self,*params, **keys):
        if self.base is None : self.base = super(DBase,self).__call__(*params, **keys)
        return self.base
    ##
    #####################################################
    # 方法:: DBase :: insert
    # --------------------------------------------------
    # 描述:: 数据库插入方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : tableName :: 数据库表名
    # param2:in--   Array  : mapx       :: 数据字典
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : lastId :: 最后执行ID
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def insert(self,tableName,mapx):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.__getInsertStr(tableName,mapx))
            self.dbConn.commit()
            insertId=cur.lastrowid
            cur.close()
            return insertId
        except:
            print '数据库保存失败'
            cur.close()
        finally:
            cur.close()
    ##
    #####################################################
    # 方法:: DBase :: update
    # --------------------------------------------------
    # 描述:: 数据库修改方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : tableName :: 数据库表名
    # param2:in--   String : where       :: 条件字典
    # param3:in--   String : data         :: 数据字典
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def update(self,tableName,where,data):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.__getUpdateStr(tableName,where,data))
            self.dbConn.commit()
            result=cur.fetchone()
            cur.close()
            return result
        except:
            cur.close()
        finally:
            cur.close()
    ##
    #####################################################
    # 方法:: DBase :: delete
    # --------------------------------------------------
    # 描述:: 数据库删除方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : tableName :: 数据库表名
    # param2:in--   String : where       :: 条件字典
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows :: 受影响记录行
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def delete(self,tableName,where):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.__getDeleteStr(tableName,where))
            self.dbConn.commit()
            result=cur.fetchone()
            cur.close()
            return result
        except:
            cur.close()
        finally:
            cur.close()
    ##
    #####################################################
    # 方法:: DBase :: select
    # --------------------------------------------------
    # 描述:: 数据库查询方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : sqlStr :: 查询语句
    # --------------------------------------------------
    # 返回：
    # return:out--  Array : result :: 结果集
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def select(self,sqlStr):
        cur = self.dbConn.cursor()
        try:
            cur.execute(sqlStr)
            self.dbConn.commit()
            result=cur.fetchall()
            cur.close()
            return  result
        except:
            cur.close()
        finally:
            cur.close()
    ##.插入数据语句.#
    def __getInsertStr(self,table,mapx):
        sql="INSERT INTO "+str(table)+"(@keys) "+"VALUE(@vals)"
        keys=''
        vals=''
        i=0
        for x in mapx:
            if i!=0 :
                keys += ','+str(x)
                vals += ",'"+ str(mapx[x]) + "'"
            else :
                keys += str(x)
                vals += "'"+ str(mapx[x]) + "'"
            i=i+1
        return sql.replace('@keys',keys).replace('@vals',vals)
    ##.获取修改语句.#
    def __getUpdateStr(table,where,valuex):
        sql="UPDATE "+table+" SET "+"@value"+"  WHERE  "+"@where"
        wi=0
        whereStr=''
        valueStr=''
        for x in where:
            if wi!=0 :
                whereStr += '   AND    '+str(x) +"="+"'"+str(where[x])+"'"
            else :
                whereStr += str(x) + "=" + "'" + str(where[x]) + "'"
            wi=wi+1
        wi=0
        for x in valuex:
            if wi!=0 :
                valueStr += ','+str(x) +"="+"'"+str(valuex[x])+"'"
            else :
                valueStr += str(x) + "=" + "'" + str(valuex[x]) + "'"
            wi=wi+1
        return sql.replace('@where', whereStr).replace('@value', valueStr)
    ##.获取删除语句.#
    def __getDeleteStr(table,where):
        sql="DELETE FROM "+table+" WHERE   @where"
        wi=0
        whereStr=''
        valueStr=''
        for x in where:
            if wi!=0 :
                whereStr += '   AND    '+str(x) +"="+"'"+str(where[x])+"'"
            else :
                whereStr += str(x) + "=" + "'" + str(where[x]) + "'"
            wi=wi+1
        return sql.replace('@where', whereStr)

