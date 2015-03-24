from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
    data = '<html>\n<body>'
    data += '<h1>Hello word</h1>'
    data += '<h2>Parameters</h2>'

    data += '\n<ul>'

    #if method get
    if request.method == 'GET':
        parameters = request.GET.dict() 
    #if method  post
    elif request.method == 'POST':
        parameters = request.POST.dict()
    #apending parameters
    for key in parameters.keys():
        data += '\n\t<li>' + key + ' : ' + parameters[key] + '</li>'

    data += '\n</ul>'
    data += '\n</body>\n<html>'
    return HttpResponse(data)