# -*- coding:utf-8 -*-
# -引入依赖
from BaseModel import BaseModel

"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：学习使人进步，骄傲使人落后
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""
class VideoModel(BaseModel):

    tableName = 't_video'

    """
    # 初始化方法
    """
    def __init__(self, data = None):
        VideoModel.fiexdModel = [
            "id",
            "tag_id",
            "video_id",
            "user_pic",
            "user_desc",
            "user_nickname",
            "hash",
            "title",
            "type",
            "nature",
            "height",
            "width",
            "video_url",
            "video_size",
            "description",
            "video_style",
            "video_duration",
            "cover_pic",
            "create_time",
            "grad_time",
            "status",
            "operator",
            "modify_time",
            "version",
            "remark"
        ]
        super(VideoModel, self).__init__(data)