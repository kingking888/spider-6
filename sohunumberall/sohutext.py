#encoding=utf-8
import pymysql
pymysql.install_as_MySQLdb()
import requests,json,time,datetime,MySQLdb
from urllib import unquote
from lxml import etree
import hashlib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
conn = MySQLdb.connect(
    user='root',
    port=3306,
    passwd='root',
    host='47.95.36.78',
    db='jeepadmin',
    charset='utf8'
)
def getcontent():
    for page in range(1,3):
        url = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=18&page='+str(page)+'&size=20&callback=jQuery'
        content = requests.get(url).text
        content = content.replace('/**/jQuery(','')+')'
        content = content.replace(');)','')
        content = json.loads(content)
        for i in content:
            personalPage = i['personalPage']
            personalPageUrl = 'http://mp.sohu.com/apiV2/profile/newsListAjax?' + personalPage.split('?')[1] + '&pageNumber='
            getpersonalPageUrl(personalPageUrl,personalPage)
def getpersonalPageUrl(personalPageUrl,personalPage):
    try:
        for page in range(1,2):
            personalUrl = personalPageUrl + str(page) + '&pageSize=10&categoryId='
            content = requests.get(personalPage).text
            htmls = etree.HTML(content)
            user_pic = htmls.xpath('//div[@class="article_right"]//div[@class="profile_all"]/img/@src')[0]
            user_name = htmls.xpath('//p[@id="ff"]/text()')[0]
            gettexturl(personalUrl,user_pic,user_name)
    except:
        print('not enough pages')
def gettexturl(personalUrl,user_pic,user_name):
    try:
        content = requests.get(personalUrl)
        htmls = json.loads(content.json())
        data = htmls['data']
        for i in data:
            title = unquote(i['title'].decode('gbk').encode('utf-8'))
            coverpicture = i['thumbnail']
            visit = i['newsPv']
            tags = 'X'
            timex = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['postTime'] / 1000))
            for x in i['tags']:
                tags = tags + '-' + x['name']
                tag = tags
            url = 'http://' + i['url'].replace('//','')
            hash = hashlib.md5()
            hash.update(title.encode(encoding='utf-8'))
            newTitle = hash.hexdigest()
            select_table(title, coverpicture, visit, tag, timex, url,user_pic,user_name,newTitle)
    except:
        print('空')
def select_table(title, coverpicture, visit, tag, timex, url,user_pic,user_name,newTitle):
    selecturl = 'https://apipre.xiaomatv.cn/V3/Article/checkArticle?title=' +newTitle
    result = requests.get(selecturl).text
    if int(result) == 1:
        print '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + newTitle
        instert_texts(title, coverpicture, visit, tag, timex, url,user_pic,user_name,newTitle)
def instert_texts(title, coverpicture, visit, tag, timex, url,user_pic,user_name,hash):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO t_article(linkUri,title,create_time,visited_count,cover_pic,remark,user_pic,user_nickname,nature,type,hash) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (url,title,timex,visit,coverpicture,tag,user_pic,user_name,100,100,hash))
        articleId = cur.lastrowid
        index = 0
        conn.commit()
        cur.close()

    except:
        print '数据库保存失败'
        cur.close()
    finally:
        cur.close()
    gettext(url,articleId,index)
def gettext(url,articleId,index):
    content = requests.get(url).text
    htmls = etree.HTML(content)
    xpathlist = htmls.xpath('//article[@class="article"]//text() | //*[@class="article"]//img/@src  | //iframe//@src  | //*[@class="article"]/div/p/img/@src')
    for p in xpathlist:
        if len(p) <= 0:
            continue
        # 判断段落类型
        if 'sohucs' in p:
            type = 2
        elif 'iframe' in p:
            type = 3
        else:
            type = 1
        index = index + 1
        insert_table(p,articleId,index,type)
def insert_table(p,articleId,index,type):
    # 保存数据库
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO t_article_html(html,text_id,sort,type) VALUES ('%s','%s','%s','%s')" % (p,articleId,index,type))
        conn.commit()
        cur.close()
    except:
        print '数据库保存失败'
        cur.close()
    finally:
        cur.close()
#getcontent()