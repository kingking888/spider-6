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
def getNumber(*page):
    url = "https://chejiahao.autohome.com.cn/Authors/AuthorListMore?orderType=3&page=" + str(page[0]) + '&userCategory=13'
    content = requests.get(url=url, timeout=3).text
    htmls = etree.HTML(content)
    numbersurl = htmls.xpath('//div[@class="list-box"]/a/@href')
    numbersimg = htmls.xpath('//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="author-list-cover"]/img/@src')
    numbersname = htmls.xpath('//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="list-dec"]/div[1]/text()')
    for item in range(0, len(numbersurl)):
        numberurl = numbersurl[item].replace("#", '?infotype=3#')
        numberimg = numbersimg[item]
        numbername = numbersname[item]
        numberurl = 'https://chejiahao.autohome.com.cn' + numberurl
        status = getmp4linkurl(numberurl, numberimg, numbername)
        if status == 0: continue
def getmp4linkurl(numbervideourl,numberimg,numbername):
    try:
        content = requests.get(url=numbervideourl,timeout = 3 ).text
        htmls = etree.HTML(content)
        mp4linkurls = htmls.xpath('//div[@class="videoTitle"]/a/@href')
        mp4linktitles = htmls.xpath('//div[@class="videoTitle"]/a/span/text()')
        mp4imgs = htmls.xpath('//div[@class="videoImg"]/a/img/@data-original')
        views = htmls.xpath('//div[@class="videoTitle"]/div[@class="num"]/span[@class="liulan"]/text()')
        times = htmls.xpath('//div[@class="videoTitle"]/div[@class="num"]/span[@class="time"]/text()')
        status = 1
        for item in range(0,len(mp4linkurls)):
            mp4linkurl = 'https://chejiahao.autohome.com.cn' + mp4linkurls[item]
            mp4linktitle = mp4linktitles[item]
            mp4img = mp4imgs[item]
            view = views[item]
            timea = times[item]
            timea = str(timea)
            if len(timea) ==11:
                year = datetime.datetime.now().year
                timea = str(year) + '-' + timea + ':00'
                timestr = time.mktime(time.strptime(timea, "%Y-%m-%d %H:%M:%S"))
                timex = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestr))
            elif len(timea) == 16:
                timea = timea + ':00'
                timestr = time.mktime(time.strptime(timea, "%Y-%m-%d %H:%M:%S"))
                timex = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestr))
            if '万' in view:
                if '.' in view:
                    view = view.split('.')
                    view = view[0]
                    view = int(view)*10000
                else:
                    view = view.split('万')
                    view = view[0]
                    view = int(view)*10000
            else:
                view = view
            status = getmp4url(mp4linkurl,mp4linktitle,numberimg,numbername,view,timex,mp4img)
            if status == 0 : break
        return status
    except:
        pass
def getmp4url(mp4linkurl,mp4linktitle,numberimg,numbername,view,timex,mp4img):
        content = requests.get(mp4linkurl).text
        htmls = etree.HTML(content)
        scripts = htmls.xpath('//script/text()')
        status = 1
        for script in scripts:
            if 'ahplayerParms' in script:
                script = script.split('}')[0]
                script = script.split('vid: "')[-1]
                mp4id = script.split('",')[0]
                requesturl = 'https://p-vp.autohome.com.cn/api/gpi?mid=' + mp4id + '&ft=mp4'
                content = requests.get(requesturl).text
                mp4json = json.loads(content)
                result =  mp4json['result']
                media = result['media']
                qualities = media['qualities']
                qualitie = qualities[-1]
                mp4url_time = qualitie['copy']
                mp4url = mp4url_time.split('?')[0]
                video_address = '汽车之家号'
                hash = hashlib.md5()
                hash.update(mp4linktitle.encode(encoding='utf-8'))
                newTitle = hash.hexdigest()
                status = select_table(mp4url,mp4linkurl,mp4linktitle,numberimg,numbername,view,timex,mp4img,video_address,newTitle)
                if status == 0 :
                    break
        return status
def select_table(mp4url,mp4linkurl,mp4linktitle,numberimg,numbername,view,timex,mp4img,video_address,newTitle):
    selecturl = 'https://apipre.xiaomatv.cn/V3/Article/checkVideo?title=' + newTitle
    result = requests.get(selecturl).text
    if result == '1':
        print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
        insert_table(mp4url,mp4linkurl,mp4linktitle,numberimg,numbername,view,timex,mp4img,video_address,newTitle)
        return 1
    else :
        print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + 'NEXT NUMBER'
        return 0
def insert_table(mp4url,mp4linkurl,mp4linktitle,numberimg,numbername,view,timex,mp4img,video_address,hash):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO video(title,video_url,cover_pic,hash,file_name,ownner_id,create_time,video_info,status,video_address,play_count)  VALUES  ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (mp4linktitle, mp4url, mp4img, hash, numberimg, 0, timex, numbername, 5, video_address,view))
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

