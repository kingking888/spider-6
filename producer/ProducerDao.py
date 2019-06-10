# -*- coding:utf-8 -*-
#-引入依赖
import hashlib
import json
from   urllib      import unquote
from   core.DBase  import DBase
from   core.Query  import Query
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：保存数据基础类
# --------------------------------------------------
# 时间：2017-11-30
# --------------------------------------------------
"""

class ProducerDao(object):
    db = object
    
    """
    # 初始化方法
    """
    def __init__(self,config = {}) :
        self.db = DBase(config)
    """
    #####################################################
    # 方法:: ProducerDao :: article
    # ---------------------------------------------------
    # 描述:: 保存文章接口
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  :: 请求地址
    # param2:in--   string : type :: 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def article(self,tabel,url,type,nature,data,fiexd):
        try:
            title = unquote(data[fiexd['title']].decode('gbk').encode('utf-8'))
            hash = hashlib.md5()
            hash.update(title.encode(encoding='utf-8'))
            hashi = hash.hexdigest()
            if (self.check(url, hashi, type, nature)): return 0
            max = {
                "title"         : title,
                "cover_pic"     : data[fiexd['cover_pic']],
                "create_time"   : data[fiexd['create_time']],
                "linkUri"       : data[fiexd['link_url']],
                "user_nickname" : data[fiexd['user_nickname']],
                "user_pic"      : data[fiexd['user_pic']],
                "hash"          : hashi,
                "status"        : 0,
                "type"          : type,
                "nature"        : nature,
                "user_id"       : 0,
                "remark"        : data[fiexd['remark']]
            }
            try:
                return self.db.INSERT(tabel, max)
            except:
                return 0
            finally:
                pass
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: ProducerDao :: video
    # ---------------------------------------------------
    # 描述:: 获取API接口
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  :: 请求地址
    # param2:in--   string : type :: 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def video(self,tabel,url,type,nature,data,fiexd)  :
        try:
            title = unquote(data[fiexd['title']].decode('gbk').encode('utf-8'))
            hash = hashlib.md5()
            hash.update(title.encode(encoding='utf-8'))
            hashi = hash.hexdigest()
            if (self.check(url,hashi,type,nature)) : return 0
            max = {
                "title"         : title,
                "cover_pic"     : data[fiexd['cover_pic']],
                "create_time"   : data[fiexd['create_time']],
                "video_url"     : data[fiexd['video_url']],
                "video_info"    : data[fiexd['user_nickname']],
                "file_name"     : data[fiexd['user_pic']],
                "play_count"    : data[fiexd['play_count']],
                "hash"          : hashi,
                "status"        : 5,
                "ownner_id"     : 0,
                "video_address" : data[fiexd['remark']]
            }
            try:
                return self.db.INSERT(tabel, max)
            except:
                return 0
            finally:
                pass
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: ProducerDao :: check
    # ---------------------------------------------------
    # 描述:: 检测是否存在
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  :: 请求地址
    # param2:in--   string : type :: 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def check(cls,url,hash,type,nature)   :
        try:
            url = url.replace("@title",hash).replace("@type",type).replace("@nature",nature)
            res = Query.getAPI(url)
            if res == '1':
                return True
            else :
                return False
        except:
            return False
        finally:
            pass
    """
    #####################################################
    # 方法:: ProducerDao :: aHtml
    # ---------------------------------------------------
    # 描述:: 文章段落处理
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : url  :: 请求地址
    # param2:in--   string : type :: 返回类型
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def aHtml(self,url,xpath,tabel,articleId,fiexd):
        try:
            htmls = Query.getHTML(url)
            if htmls == None : return None
            tree = htmls.xpath(xpath)
            if len(tree) <= 0 : return None
            i = 1
            for x in tree :
                if len(x) <= 0 : continue
                html = {
                    "sort"    : i,
                    "html"    : x,
                    "text_id" : articleId
                }
                if fiexd['image']    in x :
                    html['type'] = 2
                elif fiexd['iframe'] in x :
                    html['type'] = 3
                else :
                    html['type'] = 1
                try:
                    self.db.INSERT(tabel,html)
                except:
                    continue
                finally:
                    pass
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法:: ProducerDao :: load
    # ---------------------------------------------------
    # 描述:: 读取配置文件
    # ---------------------------------------------------
    # 参数:
    # param1:in--   string : jsonDir  :: 配置地址
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def load(self,jsonDir):
        with open(jsonDir) as json_file:
            data = json.load(json_file)
            return data