"""
        except OSError:
            pass
"""
from QiniuYun import QiniuYun
from DBase import  DBase

#.七牛测试
QN = QiniuYun({
  "accessKey"    : "jA9IXMBf5nYpMPU4nDoL4GzS_QbEgaeXlSY8FTzz",
  "secretKey"    : "LG89eWSHaUxEvK6Bkt2YBLezqyYmWM3DgRKvdaUt",
  "bucketName"   : "7wonders",
  "resDomain"    : "px8koop6o.bkt.clouddn.com"
})

print(QN.uploadFile('0f84790e0022431c9e63427907d5eade.mp4','./download/93414332321/0f84790e0022431c9e63427907d5eade.mp4'))


DB = DBase({
"userName": "ssadmin",
"passWord": "shopshops2019#",
"localHost": "rm-2ze967w9aaqpae2e0ko.mysql.rds.aliyuncs.com",
"dataName": "spider"
})

print()