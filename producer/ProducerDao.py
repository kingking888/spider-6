# -*- coding:utf-8 -*-
#-引入依赖
import hashlib
from   urllib         import unquote
from   systems.DBase  import DBase
from   systems.Query  import Query
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
            if (self.check('article',hashi)): return 0
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
    # 描述:: 保存视频信息
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
            if (self.check("video",hashi)) : return 0
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
    def check(cls,table,hash)   :
        try:
            count = cls.db.SELECT("SELECT COUNT(1) NUM FROM " + table +  "  WHERE hash = '" + hash)
            if count[0]['NUM'] >  0 :
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