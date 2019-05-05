#encoding=utf-8
import requests,json,time,datetime,pymysql
from lxml import etree
class GetComment():
    def __init__(self):
        pass
    def getcontent(self):
        urllists = ['xinche/c1044/','xinche/c1089/','pingce/c1062/','/pingce/c1063/','wenhua/c1179/','/wenhua/c1108/','wenhua/c1107/','wenhua/c1180/','wenhua/c1181/']
        for id in range(0,len(urllists)):
            url = 'http://news.bitauto.com/' + urllists[id]
            content = requests.get(url).text
            htmls = etree.HTML(content)
            texturls = htmls.xpath('//div[@class="details"]/h2/a/@href')
            texttitles = htmls.xpath('//div[@class="details"]/h2/a/text()')
            for id in range(0,len(texturls)):
                texttitle = texttitles[id]
                textid = texturls[id].split('http://news.bitauto.com/xinchexiaoxi/')[-1].split('/')[-1].split('.html')[0]
                textidone = int(textid)/10000000
                textid = str(textidone).split('.')[-1]
                self.getcomment(textid,texttitle)
    def getcomment(self,textid,texttitle):
        print(textid,texttitle)
        commenturl = 'http://newsapi.bitauto.com/comment/comment/getdata?callback=jQuery&productId=1&objectId=' + textid + '&pageIndex=1&pageSize=10&isHot=false'
        a = requests.get(commenturl).text
        b = a.split('jQuery(')[-1].replace(');','')
        c = json.loads(b)
        try:
            result = c['result']
            commentlists = result['list']
            for commentlist in commentlists:
                print(commentlist)
                comment_one = commentlist['content']
                timestr = commentlist['createTime']
                timestr = time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S"))
                timestr = str(timestr).split('.')[0]
                print(timestr)
                requests_url = 'https://api.xiaomatv.cn/Action/submitComment?title=' + texttitle + '&status=1' + '&create_time=' + timestr + '&content=' + comment_one
                print(requests_url)
                text = requests.get(requests_url).text
                print(text)
        except:
            pass
getcomment = GetComment()
getcomment.getcontent()