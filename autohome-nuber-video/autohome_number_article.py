#encoding=utf-8
import requests
import threading
from lxml import etree
import time
import datetime
import json
import pymysql
import hashlib
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
#.find NUMBER URL
def getNumber(*page):
    url     = "https://chejiahao.autohome.com.cn/Authors/AuthorListMore?orderType=3&page=" + str(page[0]) + '&userCategory=13'
    content = requests.get(url=url,timeout =3).text
    htmls   = etree.HTML(content)
    numbersurl = htmls.xpath('//div[@class="list-box"]/a/@href')
    numbersimg = htmls.xpath('//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="author-list-cover"]/img/@src')
    numbersname = htmls.xpath('//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="list-dec"]/div[1]/text()')
    for item in range(0,len(numbersurl)):
        numberurl  = numbersurl[item].replace("#",'?infotype=1#')
        numberimg  = numbersimg[item]
        numbername = numbersname[item]
        numberurl  = 'https://chejiahao.autohome.com.cn' + numberurl
        status     = findArticle(numberurl,numbername,numberimg)
        if status == 0 : continue
#. find Article
def  findArticle (userUrl,userName,userPic):
    content = requests.get(url=userUrl, timeout=3).text
    htmls   = etree.HTML(content)
    articleUrl      = htmls.xpath('//div[@class="author-vr identclass box videoV"]/a[1]/@href')
    if len(articleUrl) <= 0 : return 0
    articleDes      = htmls.xpath('//div[@class="author-vr identclass box videoV"]/@pageid')
    articleTxt      = htmls.xpath('//div[@class="author-vr identclass box videoV"]/a[1]/div/text()')
    articlePic      = htmls.xpath('//div[@class="author-vr identclass box videoV"]/div[@class="videoA"]/div[@class="videoL fn-left"]/a[1]/img/@data-original')
    status = checkArticle(userName,userPic,articleUrl,articleTxt,articlePic,articleDes)
    if status == 0 : return 0
#.checkUrl
def checkArticle (userName,userPic,articleUrl,articleTxt,articlePic,articleDes):
    for x in range(0, len(articleUrl)):
        hash = hashlib.md5()
        hash.update(articleTxt[x].encode(encoding='utf-8'))
        newTitle  = hash.hexdigest()
        selecturl = 'https://apipre.xiaomatv.cn/V3/Article/checkArticle?title=' + newTitle
        result = requests.get(selecturl).text
        if result == '1':
            print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
            linkUrl = 'https://chejiahao.autohome.com.cn' + articleUrl[x]
            cur = conn.cursor()
            cur.execute("INSERT INTO t_article(title,`type`,linkUri,nature,create_time,user_nickname,user_pic,cover_pic,hash,remark) "
                        "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %
                        (articleTxt[x], 4, linkUrl, 100, (articleDes[x])[0:19], userName,userPic,articlePic[x],newTitle,'X'))
            articleId = cur.lastrowid
            conn.commit()
            cur.close()
            findArticleHtml(articleId ,linkUrl)
            return 1
        else:
            print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + 'NEXT NUMBER'
            return 0
#.FIND ARTICLE HTML
def findArticleHtml(articleId,articleUrl) :
    content = requests.get(url=articleUrl, timeout=3).text
    htmls   = etree.HTML(content)
    contents = htmls.xpath('//div[@class="article-content example"]/div/p/text() | //div[@class="article-content example"]/div/img/@data-original ')
    i = 0
    for x in contents :
        html = ''
        type = 0
        if x[0:1] == '/' :
            html =  x
            type = 2
        else :
            html =  x.encode(encoding='utf-8')
            type =  1
        i = i+1
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO t_article_html(text_id,type,sort,html) VALUES ('%s','%s','%s','%s')" % (articleId, type, i, html))
            cur.lastrowid
            conn.commit()
            cur.close()
        except:
            cur.close()
        finally:
            cur.close()
"""
注册100 个线程 | 处理100个分页
"""
threadx = []
params = []
for x in range(101)    : params.append(str(x))
for x in range(1,101) : threadx.append(threading.Thread( target=getNumber,args=(params[x])))
"""
100个线程 | 每次只启动5个 | 处理20次
"""
def AutoThread( index = 0):
    print "ONCE THIS ",index
    if index >=20 : return
    for x in range(5): threadx[x+(index*5)].start()
    for x in range(5): threadx[x+(index*5)].join()
    index = index + 1
    AutoThread(index)
AutoThread()