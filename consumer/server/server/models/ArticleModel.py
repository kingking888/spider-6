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
class ArticleModel(BaseModel.BaseModel):

    tableName = 't_article'

    """
    # 初始化方法
    """
    def __init__(self, data = None):
        ArticleModel.fiexdModel = [
            "id",
            "title",
            "cover_pic",
            "link_url",
            "user_nickname",
            "user_pic",
            "hash",
            "type",
            "nature",
            "create_time",
            "status",
            "operator",
            "modify_time",
            "version",
            "reamrk"
        ]
        super(ArticleModel, self).__init__(data)

