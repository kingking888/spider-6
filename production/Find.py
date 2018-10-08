# -*- coding:utf-8 -*-
import time,json
from   core.Query import Query
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：数据挖掘类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
"""

class Find():
    pass
    """
    #####################################################
    # 方法:: Find :: startWork
    # ---------------------------------------------------
    # 描述:: 获取API接口
    # ---------------------------------------------------
    # 参数:
    # param1:in--   Map    : params  :: 参数配置
    # param2:in--   Map    : config  :: 系统配置
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def startWork(cls,params = {},config = {} ):
        try:
            ##--如果参数为空就结束
            if len(params) <= 0 : return 0
            if params['resourceType'] == 4 : ##--文章类型
                if   params["requestType"] == 'API' : ##--请求类型为接口
                    requestUrl = []
                    for key in params["requestParam"].keys():
                        if len(params["requestParam"][key]) > 0 :
                            for x in params["requestParam"][key] :
                                requestUrl.append(params["resourceUri"].replace('@'+key,x))
                        else :
                            pass
                    for i in range(1,params["page"]) :
                        for url in requestUrl:
                            link = url.replace('@page',str(i))
                            result = Query().getAPI(link,params["requestBack"],params['clearStart'],params['clearLastd'])
                            if params["dataBase"] != 'NULL' : result = result[params["dataBase"]]
                            for x in result:
                                ##--any = cls.analysisJSON(params["resourceXpath"],x)
                                exit(0)
                elif params["requestType"] == 'HTML': ##--请求类型为网页
                    pass
                else : ##--请求类型为其他
                    pass
            elif params['resourceType'] == 1 : ##--视频类型
                pass
        except:
            return 0
        finally:
            pass

    """
    #####################################################
    # 方法:: Find :: analysisJSON
    # ---------------------------------------------------
    # 描述:: 解析数据
    # ---------------------------------------------------
    # 参数:
    # param1:in--   Map    : params  :: 参数配置
    # param2:in--   Map    : config  :: 系统配置
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def analysisJSON(cls,params = {},data = {}):
        try:
            muse = {}
            for key in params.keys():
                values = params[key].split('|')
                if values[1] == 'str' :         ##--字符类型
                    muse[key] = data[values[2]]
                elif values[1] == 'array' :     ##--数组类型
                    arrKey = values[2].split('->')
                    arrVal = []
                    if arrKey[1] == '0' :
                        arrVal = data[arrKey[0]][0]
                    else :
                        for x in data[arrKey[0]] : arrVal.append(x[arrKey[1]])
                    muse[key] = arrVal
                elif values[1] == 'url' :       ##--地址类型
                    muse[key] = 'http:' + data[values[2]]  if data[values[2]][0:2] == '//'  else data[values[2]]
                elif values[1] == 'time' :      ##--时间类型
                    if type(data[values[2]]) == int and data[values[2]] > 10:
                        muse[key] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data[values[2]]) / 1000))
                    else:
                        muse[key] = data[values[2]][0, 19]  if '-' in data[values[2]] else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                elif values[1] == 'set'  :      ##--重置类型
                    arrKey = values[2].split('=>')
                    setKey = arrKey[0].split('+')
                    for x in setKey :
                        arrKey[1] = arrKey[1].replace('@'+x,str(data[x]))
                    muse[key] = arrKey[1]
                elif values[1] == 'int'  :      ##--数组类型
                    muse[key] = 0 if values[2] == '0' else data[values[2]]
                elif values[1] == 'def' :       ##--默认类型
                    muse[key] = None if values[2] == 'NULL' else values[2]
                elif values[1] == 'link':       ##--取参类型
                    arrKey = values[2].split('->')
                    start = data[arrKey[0]].find(arrKey[0]+'=')
                    lastd = data[arrKey[0]].find('&',start)
                    muse[key] = data[arrKey[0]][start+len(arrKey[0]+'='):lastd] if lastd != -1 else data[arrKey[0]][start+len(arrKey[0]+'='):]
                elif values[1] == 'json' :      ##--JSON类型
                    pass
                else:                           ##--其他类型
                    pass
            return muse
        except:
            return None
        finally:
            pass

    """
    #####################################################
    # 方法:: Find :: load
    # ---------------------------------------------------
    # 描述:: 读取配置文件
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : jsonDir  :: 配置地址
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def load(self,jsonDir):
        with open(jsonDir) as json_file:
            data = json.load(json_file)
            return data
