# -*- coding:utf-8 -*-
#-引入依赖
import requests
from lxml import etree
from urllib import unquote
import time
import datetime
import hashlib
import random
import json
from DBaseClass import DBase
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

##
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：爬虫抓取标签类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
##

class Keep(object):
    #.请求头部
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
    #.文本对象
    contents=''
    #.数据库操纵对象
    airawn = object
    def __init__(self,userName,passWord,localHost,dataName):
        self.airawn = DBase(userName,passWord,localHost,dataName)
    #.获取文章内容
    def  getContents(self,uri,type):
        self.contents = requests.get(uri,self.header)
        if type==1 :

            self.contents = json.loads(self.contents.json())
        else :
            self.contents = self.contents.text
        return self.contents
    #.获取文章列表
    def   getArticles(self,maps,checkUri,type,nature):
        result=[]
        for i in maps['data']:
            title = unquote(i['title'].decode('gbk').encode('utf-8'))
            hash = hashlib.md5()
            hash.update(title.encode(encoding='utf-8'))
            newTitle = hash.hexdigest()
            content =self.getContents(checkUri.replace("@title",newTitle).replace("@type",type).replace("@nature",nature),2)
            if content == '0' :
               break
            else :
                mapx = {}
                mapx['title'] = title
                mapx['hash'] = newTitle
                mapx['type'] = type
                mapx['nature'] = nature
                mapx['linkUri'] = 'http:' + i['url']
                mapx['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['postTime'] / 1000))
                mapx['cover_pic'] = i['thumbnail']
                tags = 'X'
                for x in i['tags'] : tags = tags + '-' + x['name']
                mapx['remark'] = tags
                result.append(mapx)
                print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
        return result
    #.执行入段落入库操作
    def getResults(self,xpath,uri,table,articleId,muse):
        index = muse
        htmls = etree.HTML(self.getContents(uri,2))
        xpath_list = htmls.xpath(xpath)
        # .遍历获取段落标记
        for p in xpath_list:
            if len(p) <= 0:
                continue
            mapx={}
            if 'sohucs' in p:
                mapx['type'] = 2
            elif 'iframe' in p:
                mapx['type'] = 3
            else:
                mapx['type'] = 1
            mapx['sort']=index
            mapx['html']=p
            mapx['text_id']=articleId
            self.airawn.insert(table, mapx)
            index = index + 1
        return index
    #.程序主入口
    def mainx(self,linkUri,xpath,checkUri,articleTable,table,type,nature) :
        status=1
        for x in range(1, 1001):
            result=self.getArticles(self.getContents(linkUri.replace("@page",str(x)),1),checkUri,type,nature)
            if len(result)<=0 :
                status=2
                break
            else:
                for item in range(0, len(result)):
                    lastId=self.airawn.insert('t_article',result[item])
                    index=1
                    index = self.getResults(xpath,result[item]['linkUri'],table,lastId,index)
        return status
    #.读取配置文件
    def load(self,jsonDir):
        with open(jsonDir) as json_file:
            data = json.load(json_file)
            return data

