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
    ret= {
        'retCode' : 200,
        'retMsgs' : 'successful',
        'retData' : service.getRecommend(12)
    }
    return JsonResponse(ret)
