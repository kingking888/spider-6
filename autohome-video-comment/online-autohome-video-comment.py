#encoding=utf-8
import requests,json,time,datetime,pymysql
from lxml import etree
class GetComment():
    def __init__(self):
        self.ids = ['23', '21', '37', '1', '5', '16', '28', '3', '2', '29', '19', '13', '36', '35', '17', '11', '7', '24', '18',
           '30', '34', '25', '22']
    def gettitleurl(self):
        for id in range(0, len(self.ids)):
            for page in range(1, 3):
                url = "https://v.autohome.com.cn/general/" + self.ids[id] + '-' + str(page) + '-1'
                idnumber = self.ids[id]
                content = requests.get(url).text
                htmls = etree.HTML(content)
                urls = htmls.xpath('//div[@class="video-item-tit"]/a/@href')
                titles = htmls.xpath('//div[@class="video-item-tit"]/a/text()')
                times = htmls.xpath('//div[@class="video-item"]/div[last()]/span[last()]/text()')
                views = htmls.xpath('//div[@class="video-item"]/div[last()]/span[@class="count-eye"]/text()')
                comments = htmls.xpath('//div[@class="video-item"]/div[last()]/span[@id="video_38369"]/text()')
                videotimes = htmls.xpath('//div[@class="video-list-pic"]//span[@class="video-time"]/text()')
                for item in range(0, len(urls)):
                    linkurl = 'https://v.autohome.com.cn' + urls[item]
                    linkurl = linkurl.replace('.html#pvareaid=106416', '').replace('https://v.autohome.com.cn/v-', '')
                    url = 'https://reply.autohome.com.cn/api/comments/show.json?id=' + linkurl + '&page=1&appid=4&count=20&datatype=jsonp&callback=jQuery'
                    title = titles[item]
                    timex = times[item]
                    view = views[item]
                    if '.' in view:
                        view = int(view.split('.')[0]) * 10000
                    else:
                        view = view
                    comment = comments[item]
                    videotime = videotimes[item]
                    print(url, title, timex, view, comment, videotime, page, idnumber)
                    self.getcontent(url, title, timex)
    def getcontent(self,url, title, timex):
        print(url, title, timex)
        content = requests.get(url).text
        print(content)
        content = content.replace('jQuery(', '').replace('})', '') + '}'
        content = json.loads(content)
        try:
            commentlist = content['commentlist']
            print(commentlist)
            for comment in commentlist:
                comment_one = comment['RContent']
                timestr = str(comment['RReplyDate'])
                # username = comment['RMemberName']
                # userid = comment['RMemberId']
                # userid_url = 'https://i.autohome.com.cn/' + str(userid)
                # user_pic = etree.HTML(requests.get(userid_url).text).xpath('//div[@class="userHead"]/a/img/@src')[0]
                timestr = timestr.split('-')[0].replace('/Date(', '').split('+')[0]
                timestr = float(timestr) / 1000
                timestr = str(timestr).split('.')[0]
                requests_url = 'https://api.xiaomatv.cn/Action/submitComment?title=' + title + '&status=2' + '&create_time=' + timestr + '&content=' + comment_one
                print(requests_url)
                text = requests.get(requests_url).text
                print(text)
        except:
            print('评论为空的')
getcomment = GetComment()
getcomment.gettitleurl()