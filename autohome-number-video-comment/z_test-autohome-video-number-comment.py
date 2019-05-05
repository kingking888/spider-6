#encoding=utf-8
import requests
from lxml import etree
import json
import time
import datetime
import pymysql
conn = pymysql.connect(
    user='root',
    port=3306,
    passwd='root',
    host='47.95.36.78',
    db='jeepadmin',
    charset='utf8'
)
def getnumber():
    for page in range(1,6):
        url = "https://chejiahao.autohome.com.cn/Authors/AuthorListMore?orderType=3&page=" + str(page) + '&userCategory=13'
        print(url)
        content = requests.get(url=url,timeout =3).text
        htmls = etree.HTML(content)
        numbersurl = htmls.xpath('//div[@class="list-box"]/a/@href')
        numbersimg = htmls.xpath('//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="author-list-cover"]/img/@src')
        numbersname = htmls.xpath('//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="list-dec"]/div[1]/text()')
        print(len(numbersurl),len(numbersimg),len(numbersname))
        for item in range(0,len(numbersurl)):
            numberurl = numbersurl[item]
            numberimg = numbersimg[item]
            numbername = numbersname[item]
            numberurl = 'https://chejiahao.autohome.com.cn' + numberurl
            getnumbertext(numberurl,numberimg,numbername)
def getnumbertext(numberurl,numberimg,numbername):
    content = requests.get(url = numberurl,timeout = 3).text
    htmls = etree.HTML(content)
    numbertextourl  = htmls.xpath('//ul[@class="author-tag"]/a[@data-infotype="3"]/@href')
    numbertextourl =  numbertextourl[0]
    numberurl = numberurl.split('#')[0]
    numbertexturl  = numberurl + numbertextourl

    geturl(numbertexturl)
def geturl(numbertexturl):
    print(numbertexturl)
    content = requests.get(numbertexturl).text
    htmls = etree.HTML(content)
    urls = htmls.xpath('//div[@class="video identclass"]/div[@class="videoTitle"]/a/@href')
    titles = htmls.xpath('//div[@class="video identclass"]/div[@class="videoTitle"]/a/span[@class="userTitle"]/text()')
    times = htmls.xpath('//div[@class="video identclass"]/div[@class="videoTitle"]/div[@class="num"]/span[last()]/text()')
    for item in range(0,len(urls)):
        url = urls[item]
        title = titles[item]
        timea = times[item]
        print(timea)
        timea = str(timea)
        if len(timea) == 11:
            year = datetime.datetime.now().year
            timea = str(year) + '-' + timea + ':00'
            timestr = time.mktime(time.strptime(timea, "%Y-%m-%d %H:%M:%S"))
            timex = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestr))
        elif len(timea) == 16:
            timea = timea + ':00'
            timestr = time.mktime(time.strptime(timea, "%Y-%m-%d %H:%M:%S"))
            timex = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestr))
        url = url.replace('/info/','')
        url = 'https://reply.autohome.com.cn/api/comments/show.json?id=' + url + '&page=1&appid=21&count=20&datatype=jsonp&callback=jsonpCallback'
        select_table(url,title,timex)
def select_table(url, title, timex):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM t_article_comment_x WHERE title = '%s'" % (title))
        result = cur.fetchall()
        print(result)
        print(len(result))
        conn.commit()
        cur.close()
        if len(result) == 1:
            return
        elif len(result) == 0:
            getcontent(url, title, timex)
    except:
        print('操作失败')
        cur.close()
    finally:
        cur.close()
def getcontent(url,title,timex):
    print(url,title,timex)
    content = requests.get(url).text
    content =  content.replace('jsonpCallback(','').replace('})','') + '}'
    content = json.loads(content)
    try:
        commentlist = content['commentlist']
        print(commentlist)
        for comment in commentlist:
            comment_one = comment['RContent']
            timestr = str(comment['RReplyDate'])
            username = comment['RMemberName']
            userid = comment['RMemberId']
            userid_url = 'https://i.autohome.com.cn/' + str(userid)
            user_pic = etree.HTML(requests.get(userid_url).text).xpath('//div[@class="userHead"]/a/img/@src')[0]
            timestr = timestr.split('-')[0].replace('/Date(','').split('+')[0]
            timestr = float(timestr)/1000
            timea = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestr))
            insert_table(comment_one,timea,username,title,user_pic)
    except:
        print('评论为空的')
def insert_table(comment_one,timea,username,title,user_pic):
    # 保存数据库
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO t_article_comment_x(title,user_id,article_id,user_nickname,user_pic,comment_content,create_time,status,request_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (title,0,0,username,user_pic,comment_one,timea,2,2))
        conn.commit()
        cur.close()
    except:
        print ('数据库保存失败')
        cur.close()
    finally:
        cur.close()
getnumber()