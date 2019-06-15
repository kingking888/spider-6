# -*- coding:utf-8 -*-
from systems.DBase import DBase
from systems.Mongo import Mongo
"""
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：学习使人进步，骄傲使人落后
# --------------------------------------------------
# 时间：2019-01-01
# --------------------------------------------------
"""
class BaseModel(object):

    arrayModel = {}
    fiexdModel = []

    """
    # 初始化方法
    """
    def __init__(self, data = None):
        if data <> None :
            index = 0
            for i in data :
                self.arrayModel[self.fiexdModel[index]] = i
                index+=1

    """
    # 魔术方法
    """
    def __getattr__(self, name):
        print name
        if self.check(name)  and self.arrayModel.has_key(name):
            return self.arrayModel.get(name)
        else:
            return False


    """
    # 魔术方法
    """
    def __setattr__(self, name, value):
        if self.check(name):
            return self.arrayModel.setdefault(name,value)
        else:
            return False

    """
    # 魔术方法
    """
    def __delattr__(self, name):
        if self.check(name)  and self.arrayModel.has_key(name):
            return self.arrayModel.pop(name)
        else:
            return False
        pass

    """
    # 魔术方法
    """
    def check(self,name):
        if len(self.fiexdModel) == 1:
            if self.fiexdModel[0] == name :
                return True
            return False
        exists = False
        for x in self.fiexdModel:
            if x == name :
                exists = True
                break
        return exists

    """
    # 魔术方法
    """
    def get(self):
        if len(self.arrayModel) > 0 :
            return self.arrayModel
        else:
            return {}

