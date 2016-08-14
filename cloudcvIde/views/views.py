from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import yaml
from datetime import datetime
import random, string
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from jsonToPrototxt import jsonToPrototxt


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def index(request):
    return render(request, 'cloudcvIde/index.html')


@csrf_exempt
def exportToCaffe(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        prototxt = jsonToPrototxt(net)
        randomId=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
        with open(BASE_DIR+'/media/prototxt/'+randomId+'.prototxt', 'w') as f:
            f.write(prototxt)
        return JsonResponse({'id': randomId, 'name': randomId+'.prototxt', 'url': '/media/prototxt/'+randomId+'.prototxt'})


@csrf_exempt
def exportToTensorflow(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        prototxt = jsonToPrototxt(net)
        randomId=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
        with open(BASE_DIR+'/media/prototxt/'+randomId+'.prototxt', 'w') as f:
            f.write(prototxt)
        os.system('python '+BASE_DIR+'/caffe-tensorflow-master/convert.py '+BASE_DIR+'/media/prototxt/'+randomId+'.prototxt --code-output-path='+BASE_DIR+'/media/tensorflow/'+randomId+'.py')
        return JsonResponse({'id': randomId, 'name': randomId+'.py', 'url': '/media/tensorflow/'+randomId+'.py'})

