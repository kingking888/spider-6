# -*- coding: utf-8 -*-

import os
import sys, getopt
import copy
import hashlib
import codecs
import requests
import re
import json
import datetime
import time
from bson import ObjectId
from lxml import etree
from QiniuYun import QiniuYun
from DBase import  DBase


TIMEOUT = 30

RETRY = 5

THREADS = 10

noFavorite = False

QnConf = {
    "accessKey"    : "jA9IXMBf5nYpMPU4nDoL4GzS_QbEgaeXlSY8FTzz",
    "secretKey"    : "LG89eWSHaUxEvK6Bkt2YBLezqyYmWM3DgRKvdaUt",
    "bucketName"   : "7wonders",
    "resDomain"    : "http://7wonders.static.shopshops.top/"
}

DBConf = {
    "userName": "ssadmin",
    "passWord": "shopshops@china2017",
    "localHost": "rm-2ze8stl04io5382803o.mysql.rds.aliyuncs.com",
    "dataName": "live"
}

HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) "
                  "Version/11.0 Mobile/15A372 Safari/604.1",
}

QN = QiniuYun(QnConf)

DB = DBase(DBConf)


"""
#####################################################
# 方法: Fetch :getHTML
# ---------------------------------------------------
# 描述: 获取网页数据
# ---------------------------------------------------
# 参数:
# param1:in--   string : url  : 请求地址
# param2:in--   string : type : 返回类型
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def getHTML(url):
    try:
        contents = requests.get(url, HEADERS).content
        htmls = etree.HTML(contents)
        return htmls
    except BaseException as e:
        return None
    finally:
        pass


"""
#####################################################
# 方法: Douyin : load
# ---------------------------------------------------
# 描述: 读取配置文件
# ---------------------------------------------------
# 参数:
# param1:in--   string : jsonDir  : 配置地址
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def load(jsonDir):
    with open(jsonDir) as json_file:
        data = json.load(json_file)
        return data

"""
#####################################################
# 方法: Douyin : checkVideo
# ---------------------------------------------------
# 描述: 读取配置文件
# ---------------------------------------------------
# 参数:
# param1:in--   string : awemeId  : 唯一ID
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def checkVideo(awemeId):
    num = 0
    for x in DB.SELECT("SELECT COUNT(1) NUM "
                       "  FROM video "
                       " WHERE video_source = 2 AND hash='%s'" % str(awemeId)) :
        for i in x :
            num = i
    return True if num > 0 else False

"""
#####################################################
# 方法: Douyin : insertVideo
# ---------------------------------------------------
# 描述: 插入数据库
# ---------------------------------------------------
# 参数:
# param:in--   data : ...data  : 数据
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def insertVideo(userId,fname,uri,cover,awemeId,height,width,size,filePath,dytk):
    result = QN.uploadFile(uri, filePath)
    """先上传文件 | 后插入数据 | 最后删除文件"""
    if result != None and len(result['key']) :
        """数据库插入"""
        fiexd = {}
        fiexd['id'] = str(ObjectId())
        fiexd['title'] = fname
        fiexd['user_pic_url'] = QnConf['resDomain'] + dytk['uimg']
        fiexd['user_pic_key'] = dytk['uimg']
        fiexd['cover_pic_key'] = 'cover_image_' + uri + '?imageView2/1/format/png'
        fiexd['cover_pic_url'] = cover
        fiexd['video_url'] = ''
        fiexd['video_key'] = uri
        fiexd['description'] = ''
        fiexd['user_nickname'] = dytk['name']
        fiexd['user_desc'] = dytk['desc']
        fiexd['hash'] = awemeId
        fiexd['height'] = height
        fiexd['width'] = width
        fiexd['video_size'] = size
        fiexd['video_duration'] = 15
        fiexd['video_source'] = 2
        fiexd['video_nature'] = userId
        fiexd['deleted'] = 0
        fiexd['create_time'] = int(time.time()) * 1000
        fiexd['operator'] = "SYSTEM"
        fiexd['remark'] = ""
        fiexd['version'] = 1
        DB.INSERT('video', fiexd)
        if os.path.exists(filePath) :
            print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 删除本地视频路径： %s" % str(filePath))
            os.remove(filePath)
        #.先更新视频，封面如果失败，可以取首帧图
        DB.UPDATE('video', {'id': fiexd['id']}, {
            'update_time': int(time.time()) * 1000,
            'video_url': QnConf['resDomain'] + result['key']
        })
        # .上传封面
        retImg = QN.fetchFile('cover_image_' + uri, cover)
        #. 补偿机制
        if retImg != None and retImg['fsize'] > 0:
            DB.UPDATE('video', {'id': fiexd['id']}, {
                'cover_pic_url': QnConf['resDomain'] + 'cover_image_' + uri +
                                 '?imageView2/1/format/png',
                'cover_pic_key' : uri + '?imageView2/1/format/png'
            })
        else :
            DB.UPDATE('video', {'id': fiexd['id']}, {
                'cover_pic_key': result['key'] + '?vframe/jpg/offset/1',
                'cover_pic_url': QnConf['resDomain'] + result['key'] +
                                 '?vframe/jpg/offset/1'
            })

"""
#####################################################
# 方法: Douyin : download
# ---------------------------------------------------
# 描述: 下载视频
# ---------------------------------------------------
# 参数:
# param:in--   data : ...data  : 数据
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def download(mediumType, uri, mediumUrl, targetFolder, fname,userId,height,width,cover,awemeId,dytk):
    try:
        if checkVideo(awemeId):
            print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 过滤存在的视频： %s" % str(awemeId))
            return None
        headers = copy.copy(HEADERS)
        fileName = uri
        if mediumType == 'video':
            fileName += '.mp4'
            headers['user-agent'] = 'Aweme/27014 CFNetwork/974.2.1 Darwin/18.0.0'
        else:
            return None
        filePath = os.path.join(targetFolder, fileName)
        if os.path.isfile(filePath): os.path.getsize(filePath)
        retry_times = 0
        try:
            resp = requests.get(mediumUrl, headers=headers, stream=True, timeout=TIMEOUT)
        except:
            resp = None
        if resp == None: return None
        rHeader = resp.headers
        size = rHeader['Content-Length']
        if resp.status_code == 403: return None
        if int(size) <= 0: return None
        with open(filePath, "wb") as f:
            f.write(resp.content)
        print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 成功下载的视频： %s" % uri)
        f.close()
        insertVideo(userId, fname, uri, cover, awemeId, height, width, size, filePath, dytk)
        print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 已经上传的视频： %s" % uri)
        retry_times += 1
        """小憩一秒"""
        time.sleep(1)
    except BaseException as e:
        raise e
    return None

"""
#####################################################
# 方法: Douyin : getRealAddress
# ---------------------------------------------------
# 描述: 获取真实地址
# ---------------------------------------------------
# 参数:
# param:in--   data : ...data  : 数据
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def getRealAddress(url):
    if url.find('v.douyin.com') < 0: return url
    res = requests.get(url, headers=HEADERS, allow_redirects=False)
    return res.headers['Location'] if res.status_code == 302 else None

"""
#####################################################
# 方法: Douyin : getDytk
# ---------------------------------------------------
# 描述: 获取抖音TOKEN
# ---------------------------------------------------
# 参数:
# param:in--   data : ...data  : 数据
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def getDytk(url):
    res = requests.get(url, headers=HEADERS)
    if not res: return None
    dytk = re.findall("dytk: '(.*)'", res.content.decode('utf-8'))
    uimg = re.findall('<img class="avatar" src="(.*)"> </span>',res.content.decode('utf-8'))
    name = re.findall('<p class="nickname">(.*)</p><p class="shortid">', res.content.decode('utf-8'))
    desc = re.findall('<p class="signature">(.*)</p><p class="follow-info">', res.content.decode('utf-8'))
    if len(desc) <= 0:
        desc = re.findall('<p class="signature">(.*)', res.content.decode('utf-8'))
    if len(dytk):
        retImg = QN.fetchFile('user_pic_image_' + dytk[0], uimg[0])
        if retImg['fsize'] > 0:
            return {
                'dytk':dytk[0],
                'name':name[0],
                'desc':desc[0],
                'uimg':'user_pic_image_' + dytk[0]
            }
    return None

"""
#####################################################
# 方法: Douyin : usage
# ---------------------------------------------------
# 描述: 运行前检测
# ---------------------------------------------------
# 参数:
# param:in--   data : ...data  : 数据
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def usage():
    print(u"未找到share-url.txt文件，请创建.\n"
          u"请在文件中指定抖音分享页面URL，并以 逗号/空格/tab/表格鍵/回车符 分割，支持多行.\n"
          u"保存文件并重试.\n\n"
          u"例子: url1,url12\n\n"
          u"或者直接使用命令行参数指定站点\n"
          u"例子: python amemv-video-ripper.py url1,url2")

"""
#####################################################
# 方法: Douyin : parseSites
# ---------------------------------------------------
# 描述: 文件转码方法
# ---------------------------------------------------
# 参数:
# param:in--   data : ...data  : 数据
# ---------------------------------------------------
# 返回：
# return:out--  obejct : content
# ---------------------------------------------------
# 日期:2018.01.12  Add by zwx
#####################################################
"""
def parseSites(fileName):
    with open(fileName, "rb") as f:
        txt = f.read().rstrip().lstrip()
        txt = codecs.decode(txt, 'utf-8')
        txt = txt.replace("\t", ",").replace("\r", ",").replace("\n", ",").replace(" ", ",")
        txt = txt.split(",")
    numbers = list()
    for raw_site in txt:
        site = raw_site.lstrip().rstrip()
        if site:
            numbers.append(site)
    return numbers

"""
下载执行的类
"""
class CrawlerScheduler(object):
    def __init__(self, items):
        self.numbers = []
        self.challenges = []
        self.musics = []
        for i in range(len(items)):
            url = getRealAddress(items[i])
            print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 已经获取的链接： \n%s" % url)
            if not url: continue
            if re.search('share/user', url): self.numbers.append(url)
            if re.search('share/challenge', url): self.challenges.append(url)
            if re.search('share/music', url): self.musics.append(url)
        self.scheduling()

    @staticmethod
    def generateSignature(value):
        p = os.popen('node fuck-byted-acrawler.js %s' % value)
        return p.readlines()[0]

    @staticmethod
    def calculateFileMd5(filename):
        hmd5 = hashlib.md5()
        fp = open(filename, "rb")
        hmd5.update(fp.read())
        return hmd5.hexdigest()

    """
    启动程序
    """
    def scheduling(self):
        for url in self.numbers: self.download_user_videos(url)
        for url in self.challenges: self.download_challenge_videos(url)
        for url in self.musics: self.download_music_videos(url)

    """
    下载用户VIDEO
    """
    def download_user_videos(self, url):
        number = re.findall(r'share/user/(\d+)', url)
        if not len(number): return
        data = getDytk(url)
        print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 已经获取的口令： \n%s" % str(data))
        if not data['dytk']: return
        user_id = number[0]
        self._download_user_media(user_id,data,url)

    """
    下载合拍视频
    """
    def download_challenge_videos(self, url):
        challenge = re.findall('share/challenge/(\d+)', url)
        if not len(challenge): return
        challenges_id = challenge[0]
        self._download_challenge_media(challenges_id, url)

    """
    下载音乐视频
    """
    def download_music_videos(self, url):
        music = re.findall('share/music/(\d+)', url)
        if not len(music): return
        musics_id = music[0]
        self._download_music_media(musics_id, url)

    """
    放入下载队列 | 已经改为顺序执行
    """
    def _join_download_queue(self, aweme,targetFolder,userId,dytk):
        try:
            if aweme.get('video', None):
                uri     = aweme['video']['play_addr']['uri']
                fname   = aweme['share_info']['share_desc']
                height  = aweme['video']['height']
                width   = aweme['video']['width']
                cover   = aweme['video']['cover']['url_list'][0]
                awemeId = aweme['aweme_id']
                if fname.strip() == '':
                    fname = aweme['video']['play_addr']['uri']
                download_url = "https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&" \
                               "line=0&ratio=540p&watermark=1&media_type=4&vr_type=0&" \
                               "improve_bitrate=0&logo_name=aweme_self" % uri
                if aweme.get('hostname') == 't.tiktok.com':
                    download_url = 'http://api.tiktokv.com/aweme/v1/play/?{0}'
                download('video',uri,download_url,targetFolder,fname,userId,height,width,cover,awemeId,dytk)
        except BaseException as e:
            raise e

    """
    下载其他媒体
    """
    def __download_favorite_media(self, user_id, dytk, hostname, signature, favorite_folder, video_count):
        if not os.path.exists(favorite_folder):
            os.makedirs(favorite_folder)
        favorite_video_url = "https://%s/aweme/v1/aweme/favorite/" % hostname
        favorite_video_params = {
            'user_id': str(user_id),
            'count': '21',
            'max_cursor': '0',
            'aid': '1128',
            '_signature': signature,
            'dytk': dytk
        }
        max_cursor = None
        while True:
            if max_cursor:
                favorite_video_params['max_cursor'] = str(max_cursor)
            res = requests.get(favorite_video_url, headers=HEADERS, params=favorite_video_params)
            contentJson = json.loads(res.content.decode('utf-8'))
            favorite_list = contentJson.get('aweme_list', [])
            for aweme in favorite_list:
                try:
                    self._join_download_queue(aweme, favorite_folder, user_id)
                except BaseException as err:
                    raise err
                video_count += 1
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
            else:
                break
        return video_count


    """
    下载用户媒体
    """
    def _download_user_media(self, user_id, dytk, url):
        current_folder = os.getcwd()
        targetFolder = os.path.join(current_folder, 'download/%s' % user_id)
        if not os.path.isdir(targetFolder):
            os.mkdir(targetFolder)
        if not user_id:
            return
        routre = str(url).replace('https://','').replace('http://','').split('/')
        signature = self.generateSignature(str(user_id))
        user_video_url = "https://%s/aweme/v1/aweme/post/" % routre[0]
        user_video_params = {
            'user_id': str(user_id),
            'count': '21',
            'max_cursor': '0',
            'aid': '1128',
            '_signature': signature,
            'dytk': dytk['dytk']
        }
        max_cursor, video_count = None, 0
        while True:
            res = requests.get(user_video_url, headers=HEADERS, params=user_video_params)
            if max_cursor :
                user_video_params['max_cursor'] = str(max_cursor)
            contentJson = json.loads(res.content.decode('utf-8'))
            aweme_list = contentJson.get('aweme_list', [])
            if len(aweme_list) <= 0 : continue
            print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] 已经获取的数据： %s" % str(
                len(aweme_list)
            ) + "个视频资源")
            for aweme in aweme_list:
                self._join_download_queue(aweme, targetFolder,user_id,dytk)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
            else:
                break
        return video_count

    """
    下载合拍媒体
    """
    def _download_challenge_media(self, challenge_id, url):
        if not challenge_id : return
        current_folder = os.getcwd()
        targetFolder = os.path.join(current_folder, 'download/#%s' % challenge_id)
        if not os.path.isdir(targetFolder):
            os.mkdir(targetFolder)
        routre = str(url).replace('https://', '').replace('http://', '').split('/')
        signature = self.generateSignature(str(challenge_id) + '9' + '0')
        challenge_video_url = "https://%s/aweme/v1/challenge/aweme/" % routre[0]
        challenge_video_params = {
            'ch_id': str(challenge_id),
            'count': '9',
            'cursor': '0',
            'aid': '1128',
            'screen_limit': '3',
            'download_click_limit': '0',
            '_signature': signature
        }
        cursor, video_count = None, 0
        while True:
            if cursor:
                challenge_video_params['cursor'] = str(cursor)
                challenge_video_params['_signature'] = self.generateSignature(str(challenge_id) + '9' + str(cursor))
            res = requests.get(challenge_video_url, headers=HEADERS, params=challenge_video_params)
            try:
                contentJson = json.loads(res.content.decode('utf-8'))
            except:
                aweme_list = contentJson.get('aweme_list', [])
            if not aweme_list:
                break
            for aweme in aweme_list:
                aweme['hostname'] = routre[0]
                video_count += 1
                self._join_download_queue(aweme, targetFolder,challenge_id)
            if contentJson.get('has_more'):
                cursor = contentJson.get('cursor')
            else:
                break
        return video_count

    """
    下载音乐媒体
    """
    def _download_music_media(self, music_id, url):
        if not music_id : return
        current_folder = os.getcwd()
        targetFolder = os.path.join(current_folder, 'download/@%s' % music_id)
        if not os.path.isdir(targetFolder) : os.mkdir(targetFolder)
        routre = str(url).replace('https://', '').replace('http://', '').split('/')
        signature = self.generateSignature(str(music_id))
        music_video_url = "https://%s/aweme/v1/music/aweme/?{0}" % routre[0]
        music_video_params = {
            'music_id': str(music_id),
            'count': '9',
            'cursor': '0',
            'aid': '1128',
            'screen_limit': '3',
            'download_click_limit': '0',
            '_signature': signature
        }
        if routre[0] == 't.tiktok.com':
            for key in ['screen_limit', 'download_click_limit', '_signature']: music_video_params.pop(key)
            music_video_params['aid'] = '1180'
        cursor, video_count = None, 0
        while True:
            if cursor:
                music_video_params['cursor'] = str(cursor)
                music_video_params['_signature'] = self.generateSignature(str(music_id) + '9' + str(cursor))

            url = music_video_url.format(
                '&'.join([key + '=' + music_video_params[key] for key in music_video_params]))
            res = requests.get(url, headers=HEADERS)
            contentJson = json.loads(res.content.decode('utf-8'))
            aweme_list = contentJson.get('aweme_list', [])
            if not aweme_list: break
            for aweme in aweme_list:
                aweme['hostname'] = routre[0]
                video_count += 1
                self._join_download_queue(aweme,targetFolder)
            if contentJson.get('has_more'):
                cursor = contentJson.get('cursor')
            else:
                break
        return video_count


if __name__ == "__main__":
    content, opts, args = None, None, []
    try:
        if len(sys.argv) >= 2:
            opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["no-favorite"])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)

    if not args:
        filename = "share-url.txt"
        if os.path.exists(filename):
            content = parseSites(filename)
        else:
            usage()
            sys.exit(1)
    else:
        content = (args[0] if args else '').split(",")
    if len(content) == 0 or content[0] == "":
        usage()
        sys.exit(1)
    if opts:
        for o, val in opts:
            if o in ("-nf", "--no-favorite"):
                noFavorite = True
                break

    """执行队列方法"""
    CrawlerScheduler(content)
