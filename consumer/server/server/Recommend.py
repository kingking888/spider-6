from django.http import JsonResponse
def videos(request):
    ret= {
        'retCode' : 200,
        'retMsgs' : 'successful',
        'retData' : []
    }
    return JsonResponse(ret)
