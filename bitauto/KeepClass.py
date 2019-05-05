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
        self.contents = requests.get(uri,self.header).text
        if type==1 :
            self.contents = self.contents
        else :
            if 'html' in uri:
                x = etree.HTML(requests.get(uri, self.header).text).xpath('//div[@class="page-new-sty"]//a[last()-2]/text()')
                if len(x) > 0:
                    allNum = etree.HTML(requests.get(uri, self.header).text).xpath('//div[@class="page-new-sty"]//a[last()-2]/text()')[0]
                    allNum = int(allNum)
                    for page in range(1, (allNum)):
                        visit_url = uri
                        v_url = visit_url.replace('.html', '-') + str(page) + '.html'
                        self.contents = requests.get(v_url, self.header).text
                else:
                    self.contents=self.contents
            self.contents = self.contents
        return self.contents
    #.获取文章列表
    def getArticles(self,maps,linkUri,checkUri,type,nature):
        result=[]
        htmls = etree.HTML(maps)
        urls = htmls.xpath('//div[@class="details"]/h2/a/@href')
        titles = htmls.xpath('//div[@class="details"]/h2/a/text()')
        covpictures = htmls.xpath('//div[@class="article-card horizon"]/div/a/img/@src')
        times = htmls.xpath('//span[@class="time"]/text()')
        comments = htmls.xpath('//span[@class="comment"]/text()')
        tags = htmls.xpath('//ul[@class="list tags type-1"]/li[1]/a/text()')
        for item in range(0,len(titles)) :
            # content =self.getContents(checkUri.replace("@title",titles[item]),2)
            hash = hashlib.md5()
            hash.update(titles[item].encode(encoding='utf-8'))
            newTitle = hash.hexdigest()
            checkUri = checkUri + 'https://apipre.xiaomatv.cn/V3/Article/checkArticle?title=' + newTitle
            content = requests.get(checkUri).text
            timea = times[item]
            if content == '0':
                break
            else :
                mapx = {}
                mapx['remark'] = tags[item]
                mapx['title'] = titles[item]
                mapx['type'] = type
                mapx['hash'] = newTitle
                mapx['nature'] = nature
                mapx['linkUri'] = urls[item]
                mapx['create_time'] = timea
                mapx['cover_pic'] = covpictures[item]
                mapx['comment_count'] = comments[item]
                result.append(mapx)
                print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
        return result
    #.执行入段落入库操作
    def getResults(self,xpath,uri,table,articleId,muse):
        index = muse
        htmls = etree.HTML(self.getContents(uri, 2))
        xpath_list = htmls.xpath(xpath)
        # .遍历获取段落标记
        htmlPs = ''
        for p in xpath_list:
            if 'http' in p:
                htmlPs = htmlPs + '@'  + p + '@'
            else:
                htmlPs = htmlPs + p
        parray = htmlPs.split('@')
        for s in parray:
            if len(s) > 0:
                mapx = {}
                if 'http' in s:
                    mapx['type'] = 2
                else:
                    mapx['type'] = 1
                mapx['sort'] = index
                mapx['html'] = s
                mapx['text_id'] = articleId
                self.airawn.insert(table, mapx)
                index = index + 1
        return index
    #.程序主入口
    def mainx(self,linkUri,xpath,checkUri,articleTable,table,type,nature) :
        status=1
        for x in range(1, 1001):
            result=self.getArticles(self.getContents(linkUri.replace("@page",str(x)),1),linkUri,checkUri,type,nature)
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

