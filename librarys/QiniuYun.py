# -*- coding:utf-8 -*-
#-引入依赖
from qiniu import Auth,put_file,etag,BucketManager
class QiniuYun(object):
    ress  = object
    auth  = object
    name  = ''
    hash  = ''
    """
    # 初始化方法
    """
    def __init__(self,config = {}) :
        self.auth = Auth(config['accessKey'],config['secretKey'])
        self.name = config['bucketName']
        self.__getToken(self.name)
    """
    #####################################################
    # 方法: QiniuYun : 获取上传token
    # ---------------------------------------------------
    # 描述: 获取上传TOKEN
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
    def __getToken(self,bucketName):
        self.hash = self.auth.upload_token(bucketName)
    """
    #####################################################
    # 方法: QiniuYun : uploadFile
    # ---------------------------------------------------
    # 描述: 上传文件
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
    def uploadFile(self,key,fileDir):
        try:
            ret, info = put_file(self.hash,key,fileDir)
            assert ret['key']  == key
            assert ret['hash'] == etag(fileDir)
            return info
        except Exception, e:
            return None
        finally:
            pass
    """
    #####################################################
    # 方法: QiniuYun : fetchFile
    # ---------------------------------------------------
    # 描述: 抓取网络资源
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
    def fetchFile(self,key,fileUrl):
        try:
            ret, info = BucketManager(self.auth).fetch(fileUrl,self.name,key)
            assert ret['key'] == key
            return info
        except Exception, e:
            return None
        finally:
            pass