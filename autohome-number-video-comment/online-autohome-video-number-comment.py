#encoding=utf-8
import requests,json,time,datetime,pymysql
from lxml import etree
class GetComemnt():
    def __init__(self):
        pass
    def getnumber(self):
        for page in range(1, 6):
            url = "https://chejiahao.autohome.com.cn/Authors/AuthorListMore?orderType=3&page=" + str(
                page) + '&userCategory=13'
            print(url)
            content = requests.get(url=url, timeout=3).text
            htmls = etree.HTML(content)
            numbersurl = htmls.xpath('//div[@class="list-box"]/a/@href')
            numbersimg = htmls.xpath(
                '//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="author-list-cover"]/img/@src')
            numbersname = htmls.xpath(
                '//div[@class="list-box"]/a/div[@class="list-item"]/div[@class="list-dec"]/div[1]/text()')
            print(len(numbersurl), len(numbersimg), len(numbersname))
            for item in range(0, len(numbersurl)):
                numberurl = numbersurl[item]
                numberimg = numbersimg[item]
                numbername = numbersname[item]
                numberurl = 'https://chejiahao.autohome.com.cn' + numberurl
                self.getnumbertext(numberurl, numberimg, numbername)
    def getnumbertext(self,numberurl, numberimg, numbername):
        content = requests.get(url=numberurl, timeout=3).text
        htmls = etree.HTML(content)
        numbertextourl = htmls.xpath('//ul[@class="author-tag"]/a[@data-infotype="3"]/@href')
        numbertextourl = numbertextourl[0]
        numberurl = numberurl.split('#')[0]
        numbertexturl = numberurl + numbertextourl
        self.geturl(numbertexturl)
    def geturl(self,numbertexturl):
        print(numbertexturl)
        content = requests.get(numbertexturl).text
        htmls = etree.HTML(content)
        urls = htmls.xpath('//div[@class="video identclass"]/div[@class="videoTitle"]/a/@href')
        titles = htmls.xpath(
            '//div[@class="video identclass"]/div[@class="videoTitle"]/a/span[@class="userTitle"]/text()')
        times = htmls.xpath(
            '//div[@class="video identclass"]/div[@class="videoTitle"]/div[@class="num"]/span[last()]/text()')
        for item in range(0, len(urls)):
            url = urls[item]
            title = titles[item]
            timea = times[item]
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
            url = url.replace('/info/', '')
            url = 'https://reply.autohome.com.cn/api/comments/show.json?id=' + url + '&page=1&appid=21&count=20&datatype=jsonp&callback=jsonpCallback'
            index = 0
            self.getcontent(url, title,timex,index)
    def getcontent(self,url,title,timex,index):
        content = requests.get(url).text
        content =  content.replace('jsonpCallback(','').replace('})','') + '}'
        content = json.loads(content)
        try:
            commentlist = content['commentlist']
            print(commentlist)
            for comment in commentlist:
                print(comment)
                comment_one = comment['RContent']
                timestr = str(comment['RReplyDate'])
                username = comment['RMemberName']
                userid = comment['RMemberId']
                #userid_url = 'https://i.autohome.com.cn/' + str(userid)
                #user_pic = etree.HTML(requests.get(userid_url).text).xpath('//div[@class="userHead"]/a/img/@src')[0]
                print(comment_one)
                timestr = timestr.split('-')[0].replace('/Date(','').split('+')[0]
                timestr = float(timestr)/1000
                timestr = str(timestr).split('.')[0]
                requests_url = 'https://api.xiaomatv.cn/Action/submitComment?title=' + title + '&status=2' + '&create_time=' + timestr + '&content=' + comment_one
                print(requests_url)
                text = requests.get(requests_url).text
                print(text)
            return index
        except:
            print('评论为空的')

getcomment = GetComemnt()
getcomment.getnumber()
