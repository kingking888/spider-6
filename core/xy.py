# -*- coding:utf-8 -*-
#-引入依赖
import requests
import time
import datetime
import random
import json
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
    userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13C75'
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
      data = self.getContents('https://api.xiaomatv.cn/V3/Curvature/recommend?user_id=-1&device_info='+device,ua,1)
      for x in data['data']:
         if x['is_ad'] == "1" :
              for i in x['show_report'] :
                  #.self.getContents(i,ua,2)
                  print "AD SHOW ONCE~~~"
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
      data = self.getContents('https://api.xiaomatv.cn/V3/Followed/airGarden?type=2','',1)
      for x in data['data']:
         time.sleep(random.randint(0,9)) 
         if 'ua' in x :
            #.随机睡上几秒
            device = json.dumps(x)
            print device
            self.sunStudio(x['ua'],device)
         else :
            x = self.getDeviceInfo(x)
            device = json.dumps(x)
            print device
            self.sunStudio(x['ua'],device)
    ##
    #####################################################
    # 方法:: Napoleon :: getDeviceInfo
    # --------------------------------------------------
    # 描述:: 获取设备信息
    # --------------------------------------------------
    # 参数:
    # param1:in--    Array : json :: 设备信息
    # --------------------------------------------------
    # 返回：
    # return:out--  Array : json :: 转换后设备信息
    # --------------------------------------------------
    # 日期:2018.01.12  Add by zwx
    #####################################################
    ##
    def  getDeviceInfo(self,json):
        width = {
            "iPhone1,1" : "320:480",
            "iPhone1,2" : "320:480",
            "iPhone2,1" : "320:480",
            "iPhone3,1" : "640:960",
            "iPhone3,2" : "640:960",
            "iPhone4,1" : "640:960",
            "iPhone5,1" : "640:1136",
            "iPhone5,2" : "640:1136",
            "iPhone5,3" : "640:1136",
            "iPhone5,4" : "640:1136",
            "iPhone6,1" : "640:1136",
            "iPhone6,2" : "640:1136",
            "iPhone7,1" : "1080:1920",
            "iPhone7,2" : "750:1334",
            "iPhone8,1" : "750:1334",
            "iPhone8,2" : "1080:1920",
            "iPhone8,4" : "640:1136",
            "iPhone9,1"  : "750:1334",
            "iPhone9,2" : "1080:1920",
            "iPhone9,3" : "750:1334",
            "iPhone9,4" : "1080:1920",
            "iPhone10,1" : "750:1334",
            "iPhone10,2" : "1080:1920",
            "iPhone10,3" : "1125:2436",
            "iPhone10,4" : "750:1334",
            "iPhone10,5" : "1080:1920",
            "iPhone10,5" : "1125:2436"
         }
        model = {
            "iPhone1,1" : "iPhone 1G",
            "iPhone1,2" : "iPhone 3G",
            "iPhone2,1" : "iPhone 3GS",
            "iPhone3,1" : "iPhone 4",
            "iPhone3,2" : "Verizon iPhone 4",
            "iPhone4,1" : "iPhone 4S",
            "iPhone5,1" : "iPhone 5",
            "iPhone5,2" : "iPhone 5",
            "iPhone5,3" : "iPhone 5C",
            "iPhone5,4" : "iPhone 5C",
            "iPhone6,1" : "iPhone 5S",
            "iPhone6,2" : "iPhone 5S",
            "iPhone7,1" : "iPhone 6 Plus",
            "iPhone7,2" : "iPhone 6",
            "iPhone8,1" : "iPhone 6s",
            "iPhone8,2" : "iPhone 6s Plus",
            "iPhone8,4" : "iPhone SE",
            "iPhone9,1"  : "iPhone 7 (CDMA)",
            "iPhone9,2" : "iPhone 7 Plus (CDMA)",
            "iPhone9,3" : "iPhone 7 (GSM)",
            "iPhone9,4" : "iPhone 7 Plus (GSM)",
            "iPhone10,1" : "iPhone 8",
            "iPhone10,2" : "iPhone 8 Plus",
            "iPhone10,3" : "iPhone X",
            "iPhone10,4" : "iPhone 8",
            "iPhone10,5" : "iPhone 8 Plus",
            "iPhone10,5" : "iPhone X"
         }
        version = {
            "iPhone1,1" : "8.1.0",
            "iPhone1,2" : "8.1.0",
            "iPhone2,1" : "8.1.0",
            "iPhone3,1" : "8.1.0",
            "iPhone3,2" : "8.1.0",
            "iPhone4,1" : "8.1.0",
            "iPhone5,1" : "8.1.0",
            "iPhone5,2" : "8.1.0",
            "iPhone5,3" : "8.1.0",
            "iPhone5,4" : "8.1.0",
            "iPhone6,1" : "9.2",
            "iPhone6,2" : "9.2",
            "iPhone7,1" : "10.3.3",
            "iPhone7,2" : "10.3.3",
            "iPhone8,1" : "10.3.3",
            "iPhone8,2" : "10.3.3",
            "iPhone8,4" : "10.3.3",
            "iPhone9,1"  : "11.2.6",
            "iPhone9,2" : "11.2.6",
            "iPhone9,3" : "11.2.6",
            "iPhone9,4" : "11.2.6",
            "iPhone10,1" : "11.2.6",
            "iPhone10,2" : "11.2.6",
            "iPhone10,3" : "11.2.6",
            "iPhone10,4" : "11.2.6",
            "iPhone10,5" : "11.2.6",
            "iPhone10,5" : "11.2.6"
         }
        userAgents = {
            "11.2.6": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D100",
            "10.3.3": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60",
            "9.2": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13C75",
            "8.1.0": "Mozilla/5.0 (iPhone;CPU iPhone OS 8_1_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.4 Mobile/11B554a" 
        }
        if ',' in str(json['model']) : 
          models      = str(json['model']) 
          versionx     = str(version[str(json['model'])])
          userAgentx = str(userAgents[versionx])
          modelx      = str(model[models])
          info          = str(width[models]).split(':')
          width        = int(info[0])
          height       = int(info[1])
        else : 
          models      = str(json['model']) 
          versionx     = str(json['os_version'])
          userAgentx = str(userAgents['10.3.3'])
          modelx      = models
          width        = json['width']
          height       = json['height']
        json['os_version'] = versionx
        json['ua']           = userAgentx
        json['model']      = modelx
        json['width']       = width
        json['height']      = height 
        return json

#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
#.单例执行
Napoleon.instance().getDevice();
