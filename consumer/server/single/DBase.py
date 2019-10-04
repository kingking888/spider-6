# -*- coding:utf-8 -*-
import pymysql
import datetime

"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫数据库基础操作类
# --------------------------------------------------
# 时间：2019-09-09
# --------------------------------------------------
"""
class  DBase(object):

    #.定义链接对象
    dbConn = None

    """
    #####################################################
    # 方法 :: DBase ::__init__
    # ---------------------------------------------------
    # 描述: 数据库类初始化方法
    # ---------------------------------------------------
    # 参数:
    # param1:in--   String : userName  : 用户名
    # param2:in--   String : passWord  : 用户密码
    # param3:in--   String : localHost : 数据库地址
    # param4:in--   String : dataName  : 数据库名称
    # ---------------------------------------------------
    # 返回：
    # return:out--  无
    # ---------------------------------------------------
    # 日期:2019.09.09  Add by zwx
    #####################################################
    """
    def __init__(self,config = {}) :
        #.初始化链接对象
        self.dbConn = pymysql.connect(
            user    = config['userName'],
            port    = 3306,
            passwd  = config['passWord'],
            host    = config['localHost'],
            db      = config['dataName'],
            charset = 'utf8mb4'
        )

    """
    #####################################################
    # 方法 :: DBase :: insert
    # --------------------------------------------------
    # 描述: 数据库插入方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : tableName : 数据库表名
    # param2:in--    Array  : mapx      : 数据字典
    # --------------------------------------------------
    # 返回：
    # return:out--   Int : lastId : 最后执行ID
    # --------------------------------------------------
    # 日期:2019.09.09  Add by zwx
    #####################################################
    """
    def INSERT(self,tableName,mapx):
        cur = self.dbConn.cursor()
        try:
            sql = self.__getInsertStr(tableName,mapx)
            cur.execute(sql)
            self.dbConn.commit()
            cur.close()
            return mapx
        except:
            cur.close()
        finally:
            cur.close()

    """
    #####################################################
    # 方法 :: DBase  :: update
    # --------------------------------------------------
    # 描述: 数据库修改方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : tableName   : 数据库表名
    # param2:in--   String : where       : 条件字典
    # param3:in--   String : data        : 数据字典
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows : 受影响记录行
    # --------------------------------------------------
    # 日期:2019.09.09  Add by zwx
    #####################################################
    """
    def UPDATE(self,tableName,where,data):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.__getUpdateStr(tableName,where,data))
            self.dbConn.commit()
            result = cur.fetchone()
            cur.close()
            return result
        except:
            cur.close()
        finally:
            cur.close()

    """
    #####################################################
    # 方法: DBase : delete
    # --------------------------------------------------
    # 描述: 数据库删除方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : tableName  : 数据库表名
    # param2:in--    String : where      : 条件字典
    # --------------------------------------------------
    # 返回：
    # return:out--  Int : rows : 受影响记录行
    # --------------------------------------------------
    # 日期:2019.09.09  Add by zwx
    #####################################################
    """
    def DELETE(self,tableName,where):
        cur = self.dbConn.cursor()
        try:
            cur.execute(self.__getDeleteStr(tableName,where))
            self.dbConn.commit()
            result = cur.fetchone()
            cur.close()
            return result
        except:
            cur.close()
        finally:
            cur.close()

    """
    #####################################################
    # 方法: DBase : select
    # --------------------------------------------------
    # 描述: 数据库查询方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : sqlStr : 查询语句
    # --------------------------------------------------
    # 返回：
    # return:out--  Array : result : 结果集
    # --------------------------------------------------
    # 日期:2019.09.09  Add by zwx
    #####################################################
    """
    def SELECT(self,sqlStr):
        cur = self.dbConn.cursor()
        try:
            cur.execute(sqlStr)
            self.dbConn.commit()
            result = cur.fetchall()
            cur.close()
            return  result
        except:
            cur.close()
            return []
        finally:
            pass

    """
    #####################################################
    # 方法: DBase : select
    # --------------------------------------------------
    # 描述: 数据库查询方法
    # --------------------------------------------------
    # 参数:
    # param1:in--   String : sqlStr : 查询语句
    # --------------------------------------------------
    # 返回：
    # return:out--  Array : result : 结果集
    # --------------------------------------------------
    # 日期:2019.09.09  Add by zwx
    #####################################################
    """
    def EXECUTE(self,sqlStr):
        cur = self.dbConn.cursor()
        try:
            cur.execute(sqlStr)
            self.dbConn.commit()
            cur.close()
            return []
        except:
            cur.close()
            return []
        finally:
            pass

    """
    获取插入SQL语句 | 私有
    """
    def __getInsertStr(self,table,mapx):
        sql ="INSERT INTO " + str(table) + " (@keys) " + " VALUE(@vals) "
        keys = []
        vals = []
        i = 0
        for x in mapx:
            keys.append('`' + x + '`')
            if type(mapx[x]) == int :
                vals.append("'" + str(mapx[x]) + "'")
            elif type(mapx[x]) == None :
                vals.append('NULL')
            elif type(mapx[x]) == float :
                vals.append("'" + str(mapx[x]) + "'")
            elif type(mapx[x]) == str :
                vals.append("'" + mapx[x] + "'")
        return sql.replace('@keys',','.join(keys)).replace('@vals',','.join(vals))

    """
    获取更新SQL语句 | 私有
    """
    def __getUpdateStr(self,table,where,valuex):
        sql="UPDATE "+table+" SET "+"@value"+"  WHERE  "+"@where"
        wi=0
        whereStr=''
        valueStr=''
        for x in where:
            if wi!=0 :
                whereStr += ' AND ' + str(x) + "=" + "'" + str(where[x]) + "'"
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

    """
    获取删除SQL语句 | 私有
    """
    def __getDeleteStr(self,table,where):
        sql = "DELETE FROM " + table + " WHERE   @where"
        wi = 0
        whereStr = ''
        for x in where:
            if wi!=0 :
                whereStr += ' AND '+str(x) +"="+"'"+str(where[x])+"'"
            else :
                whereStr += str(x) + "=" + "'" + str(where[x]) + "'"
            wi = wi+1
        return sql.replace('@where', whereStr)

