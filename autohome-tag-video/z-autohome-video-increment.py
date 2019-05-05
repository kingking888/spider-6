#encoding=utf-8
import requests
import threading
from lxml import etree
import time
import datetime
import json
import hashlib
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')
conn = MySQLdb.connect(
    user='root',
    port=3306,
    passwd='root',
    host='47.95.36.78',
    db='jeepadmin',
    charset='utf8'
)
ids = ['5','7','22']

def FindVideoUrl(MINID,page):
    url = "https://v.autohome.com.cn/user/pagedata/?userid=" + MINID + "&ordertype=1&pageIndex=" + str(page) + "&istag=true"
    content = requests.get(url).text
    htmls = etree.HTML(content)
    urls = htmls.xpath('//ul[@class="channel-list active"]/li/div[@class="con"]/a/@href')
    titles = htmls.xpath('//ul[@class="channel-list active"]/li/div[@class="con"]/a/p[2]/@title')
    times = htmls.xpath('//ul[@class="channel-list active"]/li/div[@class="info"]/span[@class="athm-right"]/text()')
    covers = htmls.xpath('//ul[@class="channel-list active"]/li/div[@class="con"]/a/p[@class="scaleimg"]/picture/img/@src')
    FindVideoLink(urls, titles, times, covers)
def FindVideoLink(urls,titles,times,covers):
    for x in range(len(urls)):
        hash = hashlib.md5()
        hash.update(titles[x].encode(encoding='utf-8'))
        newTitle = hash.hexdigest()
        selecturl = 'https://apipre.xiaomatv.cn/V3/Article/checkVideo?title=' + newTitle
        result = requests.get(selecturl).text
        if int(result) == 1:
            print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
        else:
            print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + 'NEXT NUMBER'

"""
300个线程同时开干
"""
threadx = []
thready = []
threadz = []
"""
for x in range(100):
    threadx.append(threading.Thread(target=FindVideoUrl,args=('5',x+1)))
    thready.append(threading.Thread(target=FindVideoUrl,args=('7', x + 1)))
    threadz.append(threading.Thread(target=FindVideoUrl,args=('22', x + 1)))
for x in threadx:
    x.setDaemon(True)
    x.start()
    x.join(1800)
for x in thready:
    x.setDaemon(True)
    x.start()
    x.join(1800)
for x in threadz:
    x.setDaemon(True)
    x.start()
    x.join(1800)
"""