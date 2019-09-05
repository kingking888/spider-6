# -*- coding:utf-8 -*-
# -引入依赖
import hashlib
import time
import datetime
from urllib import unquote
from Fetch import Fetch
from BaseDao import BaseDao
from models.ArticleHtmlModel import ArticleHtmlModel
from models.ArticleModel import ArticleModel
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：学习使人进步，骄傲使人落后
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""
class ArticleDao(BaseDao):

    pass

    """
    # 初始化方法
    """
    def __init__(self, DBase = None,Mongo = None):
        super(ArticleDao, self).__init__(DBase,Mongo)

    """
    #####################################################
    # 方法: ArticleDao : article
    # ---------------------------------------------------
    # 描述: 保存文章接口
    # ---------------------------------------------------
    # 参数:
    # param:in--   Object : object  : 方法参数
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def insert(self, type, nature, data, fiexd):
        try:
            title = unquote(data[fiexd['title']].decode('gbk').encode('utf-8'))
            hash = hashlib.md5()
            hash.update(title.encode(encoding='utf-8'))
            hashi = hash.hexdigest()
            if (self.check(hashi)): return 0
            article               = ArticleModel()
            article.title         = title
            article.cover_pic     = data[fiexd['cover_pic']]
            article.link_url      = data[fiexd['link_url']]
            article.user_nickname = data[fiexd['user_nickname']]
            article.user_pic      = data[fiexd['user_pic']]
            article.hash          = hashi
            article.status        = 5
            article.type          = type,
            article.nature        = nature
            article.status        = 5
            article.create_time   = int(time.time())
            article.modify_time   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            article.operator      = "producer"
            article.remark        = ''
            return self.add(article)
        except Exception, e:
            return None
        finally:
            pass

    """
    #####################################################
    # 方法: ArticleDao : check
    # ---------------------------------------------------
    # 描述: 检测是否存在
    # ---------------------------------------------------
    # 参数:
    # param:in--   Object : object  : 方法参数
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def check(self,hash):
        """./consumer/server/server/sqls/checkHash.sql"""
        return self.checkHash(self.db,self.check.__doc__,ArticleModel(),hash)

    """
    #####################################################
    # 方法: ArticleDao : aHtml
    # ---------------------------------------------------
    # 描述: 文章段落处理
    # ---------------------------------------------------
    # 参数:
    # param:in--   Object : object  : 方法参数
    # ---------------------------------------------------
    # 返回：
    # return:out--  obejct : content
    # ---------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    """
    def insertHtml(self, url, xpath, tabel, articleId, fiexd):
        try:
            htmls = Fetch.getHTML(url)
            if htmls == None : return None
            tree = htmls.xpath(xpath)
            if len(tree) <= 0 : return None
            i = 1
            for x in tree:
                if len(x) <= 0:continue
                html            = ArticleHtmlModel()
                html.article_id = articleId
                html.sort       = i
                html.html       = x
                if fiexd['image'] in x:
                    html.type = 2
                elif fiexd['iframe'] in x:
                    html.type = 3
                else:
                    html.type = 1
                try:
                    self.db.INSERT(tabel, html.get())
                except:
                    continue
                finally:
                    pass
        except Exception, e:
            return None
        finally:
            pass