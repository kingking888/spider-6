# -*- coding:utf-8 -*-
#-引入依赖
import requests
import json
#from   lxml import etree
from   core.Single import Singleton

"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫网络请求基础类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
"""

class Query(object):
    #.请求头部
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
    #.文本对象
    contents=''
    """
    #####################################################
    # 方法:: Query ::getAPI
    # ---------------------------------------------------
    # 描述:: 获取API接口
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  :: 请求地址
    # param2:in--   string : type :: 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def getAPI(self,url,type = 'text',clearStart = '',clearLastd = ''):
        try:
            self.contents = requests.get(url, self.header)
            if   type == 'json':
                ##--存在需要清空的字符串
                if len(clearStart) >= 1 and len(clearLastd) >= 1:
                    contents = self.contents.text.replace(clearStart, '').replace(clearLastd, '')
                    contents = json.loads(contents)
                else :
                    contents = json.loads(self.contents.json())
            elif type == 'text':
                if len(clearStart) >= 1 and len(clearLastd) >= 1:
                    contents = self.contents.text.replace(clearStart, '').replace(clearLastd, '')
                else :
                    contents = self.contents.text
            else :
                pass
            return contents
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: Query ::getHTML
    # ---------------------------------------------------
    # 描述:: 获取网页数据
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  :: 请求地址
    # param2:in--   string : type :: 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def getHTML(self,url,type = 0):
        try:
            self.contents = requests.get(url, self.header)
            htmls = etree.HTML(self.contents)
            return htmls
        except Exception, e:
            return None
        finally:
            pass