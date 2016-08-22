from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import yaml
from datetime import datetime
import random, string
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ide.utils.jsonToPrototxt import jsonToPrototxt

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def index(request):
    return render(request, 'cloudcvIde/index.html')

@csrf_exempt
def exportToCaffe(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        net_name = request.POST.get('net_name')
        if net_name == '':
            net_name = 'Net'
        prototxt,input_dim = jsonToPrototxt(net,net_name)
        randomId=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
        with open(BASE_DIR+'/media/'+randomId+'.prototxt', 'w') as f:
            f.write(prototxt)
        return JsonResponse({'result': 'success','id': randomId, 'name': randomId+'.prototxt', 'url': '/media/'+randomId+'.prototxt'})
