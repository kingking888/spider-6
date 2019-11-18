# -*- coding: utf-8 -*-

TIMEOUT = 30

RETRY = 5

THREADS = 10

NOFAVORITE = False

QINIU_USER_CONF = {
    "accessKey"    : "jA9IXMBf5nYpMPU4nDoL4GzS_QbEgaeXlSY8FTzz",
    "secretKey"    : "LG89eWSHaUxEvK6Bkt2YBLezqyYmWM3DgRKvdaUt",
    "bucketName"   : "shopshops",
    "resDomain"    : "https://static.shopshopslive.com/"
}

QINIU_LIVE_CONF = {
    "accessKey"    : "jA9IXMBf5nYpMPU4nDoL4GzS_QbEgaeXlSY8FTzz",
    "secretKey"    : "LG89eWSHaUxEvK6Bkt2YBLezqyYmWM3DgRKvdaUt",
    "bucketName"   : "shopshops",
    "resDomain"    : "https://static.shopshopslive.com/"
}

DB_LIVE_CONF = {
    "userName": "ssadmin",
    "passWord": "shopshops@china2017",
    "localHost": "rm-2zek05a0a665a38q45o.mysql.rds.aliyuncs.com",
    "dataName": "live"
}

DB_USER_CONF = {
    "userName": "ssadmin",
    "passWord": "shopshops@china2017",
    "localHost": "rm-2zek05a0a665a38q45o.mysql.rds.aliyuncs.com",
    "dataName": "users"
}

HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) "
                  "Version/11.0 Mobile/15A372 Safari/604.1",
}
