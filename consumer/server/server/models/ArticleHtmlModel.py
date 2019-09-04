# -*- coding:utf-8 -*-
# -引入依赖
from consumer.server.server.models import  BaseModel

"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：学习使人进步，骄傲使人落后
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""
class ArticleHtmlModel(BaseModel.BaseModel):

    tableName = 't_article_html'
    """
    # 初始化方法
    """
    def __init__(self, data = None):
        super(ArticleHtmlModel,self).__init__(data)
        BaseModel.fiexdModel = [
            "id",
            "article_id",
            "type",
            "sort",
            "status",
            "html"
        ]