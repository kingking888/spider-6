# -*- coding:utf-8 -*-
#.引入依赖
import requests
import time
import datetime
import random
import json
import sys
import threading
import os
# 全局变量
start = 0
##
# --------------------------------------------------
# 作者：Mr.z@<837045534@qq.com>
# --------------------------------------------------
# 描述：刷量基础类
# --------------------------------------------------
# 时间：2018-03-18
# --------------------------------------------------
##
class Napoleon(object):
    #.请求头部
    header = object
    #.文本对象
    contents = ''
    #.默认UA
    userAgent = 'Mozilla/5.0 (Linux; Android 4.2.2; Letv X500 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36'
    #.基础对象
    base = None
    ##
    #####################################################
    # 方法:: Napoleon ::__init__
    # --------------------------------------------------
    # 描述:: 类初始化方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    无
    # --------------------------------------------------
    # 返回：
    # return:out--  无
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def __init__(self) :
       pass
    ##
    #####################################################
    # 方法:: Napoleon ::instance
    # --------------------------------------------------
    # 描述:: 类的单例方法
    # --------------------------------------------------
    # 参数:
    # param1:in--    无
    # --------------------------------------------------
    # 返回：
    # return:out--  无
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    @classmethod
    def instance(self, *params, **keys):
        if self.base is None : self.base = Napoleon(*params,**keys)
        return self.base
    ##
    #####################################################
    # 方法:: Napoleon ::getContents
    # --------------------------------------------------
    # 描述:: 获取网络请求
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : uri    :: 请求链接
    # param2:in--   String : ua    :: 请求代理
    # param3:in--   String : type  :: 请求类型
    # --------------------------------------------------
    # 返回：
    # return:out--  Object : contents :: 数据对象
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def  getContents(self,uri,ua,type):
        if ua == '' : 
          self.header = {'User-Agent' : self.userAgent}
        else :
          self.header = {'User-Agent' : ua}
        if type == 1 :
            self.contents = requests.get(uri,self.header)
            self.contents = json.loads(self.contents.text)
            return self.contents
        else :
            requests.get(uri,self.header)
            return 1
    ##
    #####################################################
    # 方法:: Napoleon :: sunStudio
    # --------------------------------------------------
    # 描述:: 曝光广告地址
    # --------------------------------------------------
    # 参数:
    # param1:in--    String : device    :: 设备信息
    # param2:in--   String : ua         :: 请求代理
    # --------------------------------------------------
    # 返回：
    # return:out--  无
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def  sunStudio(self,ua,device):
      global start
      data = self.getContents('https://api.xiaomatv.cn/V3/Curvature/recommend?user_id=-1&device_info='+device,ua,1)
      for x in data['data']:
         if x['is_ad'] == "1" :
              for i in x['show_report'] :
                  #.如果出现清空链接，跳过，不执行
                  if str(i).find('rcv.') > 0 : continue
                  self.getContents(i,ua,2)
                  start = start + 1
                  if start == 69 or start == 111 :
                      time.sleep(random.randint(1,5))
                      self.getContents(x['source_url'],ua,2)
                      print "Ad click once ~ ~ ~"
                  if start >=180 : start = 0
                  print "Ad show time " +str(start) + " yes"
         else :
              continue
    ##
    #####################################################
    # 方法:: Napoleon ::getContents
    # --------------------------------------------------
    # 描述:: 曝光大量设备
    # --------------------------------------------------
    # 参数:
    # param1:in--    无
    # --------------------------------------------------
    # 返回：
    # return:out--  无
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def   getDevice(self) :
      #.获取当前时间
      nowTime = int(datetime.datetime.now().strftime('%Y%m%d%H'))
      minDate = int(datetime.datetime.now().strftime('%Y%m%d01'))
      maxDate = int(datetime.datetime.now().strftime('%Y%m%d06'))
      if nowTime >= minDate and nowTime  <= maxDate : sys.exit(0)
      data = self.getContents('https://api.xiaomatv.cn/V3/Followed/airGarden?type=1&version=1','',1)
      for x in data['data']:
         if 'ua' in x :
            #.随机睡上几秒
            time.sleep(random.randint(1,5))
            x['version'] = 1
            device = json.dumps(x)
            print x['ua']
            self.sunStudio(x['ua'],device)
         else :
            continue
##
#####################################################
## 程序执行开始
#####################################################
##
for num in range(0,12) :
    #.单例执行
    #Napoleon.instance().getDevice()
    print num
