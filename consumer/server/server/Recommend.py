import random
from django.http import JsonResponse
from systems.DBase import DBase
from systems.Fetch import Fetch
from systems.Mongo import Mongo
from services.Funny import Funny

fetch  = Fetch()
dbase  = DBase(fetch.load('./server/config/mysql.json'))
mongo  = Mongo(fetch.load('./server/config/mongo.json'))
funny  = fetch.load('./server/config/funny.json')
def videos(request):
    global funny
    service = Funny(funny, dbase, mongo,fetch)
    data = service.getRecommend(12)
    for i in range(0,len(data)):
        data[i]['share_count'] = random.randint(500,2000)
        data[i]['thumb_count'] = random.randint(1000, 9999)
    ret= {
        'retCode' : 200,
        'retMsgs' : 'successful',
        'retData' : data
    }
    return JsonResponse(ret)
