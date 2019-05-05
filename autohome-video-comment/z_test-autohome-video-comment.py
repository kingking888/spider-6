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
ids = ['23','21','37','1','5','16','28','3','2','29','19','13','36','35','17','11','7','24','18','30','34','25','22']
def gettitleurl():
    for id in range(0,len(ids)):
        for page in range(1,3):
            url = "https://v.autohome.com.cn/general/"+ids[id]+'-'+str(page)+'-1'
            idnumber = ids[id]
            content = requests.get(url).text
            htmls = etree.HTML(content)
            urls = htmls.xpath('//div[@class="video-item-tit"]/a/@href')
            titles = htmls.xpath('//div[@class="video-item-tit"]/a/text()')
            times = htmls.xpath('//div[@class="video-item"]/div[last()]/span[last()]/text()')
            views = htmls.xpath('//div[@class="video-item"]/div[last()]/span[@class="count-eye"]/text()')
            comments = htmls.xpath('//div[@class="video-item"]/div[last()]/span[@id="video_38369"]/text()')
            videotimes = htmls.xpath('//div[@class="video-list-pic"]//span[@class="video-time"]/text()')
            for item in range(0,len(urls)):
                linkurl = 'https://v.autohome.com.cn' + urls[item]
                linkurl = linkurl.replace('.html#pvareaid=106416','').replace('https://v.autohome.com.cn/v-','')
                url = 'https://reply.autohome.com.cn/api/comments/show.json?id='+linkurl+'&page=1&appid=4&count=20&datatype=jsonp&callback=jQuery'
                title = titles[item]
                timex = times[item]
                view = views[item]
                if '.' in view:
                    view = int(view.split('.')[0])*10000
                else:
                    view = view
                comment = comments[item]
                videotime =videotimes[item]
                print(url,title,timex,view,comment,videotime,page,idnumber)
                select_table(url, title, timex)
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
    print(content)
    content =  content.replace('jQuery(','').replace('})','') + '}'
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
        cur.execute("INSERT INTO t_article_comment_x(title,user_id,article_id,user_nickname,user_pic,comment_content,create_time,status,request_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (title,0,0,username,user_pic,comment_one,timea,2,1))
        conn.commit()
        cur.close()
    except:
        print ('数据库保存失败')
        cur.close()
    finally:
        cur.close()
gettitleurl()