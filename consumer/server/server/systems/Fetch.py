# -*- coding:utf-8 -*-
#-引入依赖
import requests
import json
import lxml.etree
from Single import Singleton
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫网络请求基础类
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""

class Fetch(object):
    #.设置类型
    __metaclass__ = Singleton
    #.请求头部
    header = {
        'User-Agent': 'okhttp/3.12.3'
    }

    #.文本对象
    contents = ''

    """
    #####################################################
    # 方法: Fetch :getAPI
    # ---------------------------------------------------
    # 描述: 获取API接口
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  : 请求地址
    # param2:in--   string : type : 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def getAPI(self,url,type = 'text',clearStart = '',clearLastd = ''):
        headers = {
            'Cache-Control':"no-cache",
            'User-Agent':"PostmanRuntime/7.6.1",
            'Postman-Token':"ec149f45-d193-4a84-b699-134fdd53c745"
        }
        try:
            self.contents = requests.request("GET", url,headers=headers,timeout=(5, 10)).content
            contents = ''
            if   type == 'json':
                #--存在需要清空的字符串
                if len(clearStart) >= 1 and len(clearLastd) >= 1:
                    contents = self.contents.text.replace(clearStart, '').replace(clearLastd, '')
                    contents = json.loads(contents)
                else :
                    contents = json.loads(self.contents)
            elif type == 'text':
                if len(clearStart) >= 1 and len(clearLastd) >= 1:
                    contents = self.contents.text.replace(clearStart, '').replace(clearLastd, '')
                else :
                    contents = self.contents.text
            else :
                pass
            return contents
        except Exception as e:
            return None
        finally:
            pass

    """
    #####################################################
    # 方法: Fetch :getHTML
    # ---------------------------------------------------
    # 描述: 获取网页数据
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  : 请求地址
    # param2:in--   string : type : 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def getHTML(self,url):
        try:
            self.contents = requests.get(url, self.header).content
            htmls = etree.HTML(self.contents)
            return htmls
        except Exception as e:
            return None
        finally:
            pass

    """
    #####################################################
    # 方法: Fetch : load
    # ---------------------------------------------------
    # 描述: 读取配置文件
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : jsonDir  : 配置地址
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