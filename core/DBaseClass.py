#!/usr/bin/env python
# -*- coding:utf-8 -*-



#.  引入依赖包
import requests
from lxml import etree
from pprint import pprint
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

##
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫数据库基础操作类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
##
class  DBase(object):
    #.定义链接对象
    dbConn = object
    #.初始化爬虫类
    def __init__(self,userName,passWord,localHost,dataName):
        #.初始化链接对象
        self.dbConn = MySQLdb.connect(
            user=userName,
            port=3306,
            passwd=passWord,
            host=localHost,
            db=dataName,
            charset='utf8'
        )
    #.向数据库插入数据
    def insert(self,tableName,mapx):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.getInsertStr(tableName,mapx))
            self.dbConn.commit()
            insertId=cur.lastrowid
            cur.close()
            return insertId
        except:
            print '数据库保存失败'
            cur.close()
        finally:
            cur.close()
    #.向数据库修改数据
    def update(self,tableName,where,data):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.getUpdateStr(tableName,where,data))
            self.dbConn.commit()
            result=cur.fetchone()
            cur.close()
            return result
        except:
            cur.close()
        finally:
            cur.close()
    #.数据库删除数据
    def delete(self,tableName,where):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.getDeleteStr(tableName,where))
            self.dbConn.commit()
            result=cur.fetchone()
            cur.close()
            return result
        except:
            cur.close()
        finally:
            cur.close()
    #.数据库查询数据
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
    #.插入数据语句
    def getInsertStr(self,table,mapx):
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
    #.获取修改语句
    def getUpdateStr(table,where,valuex):
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
    #.获取删除语句
    def getDeleteStr(table,where):
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
        wi=0
        return sql.replace('@where', whereStr)

