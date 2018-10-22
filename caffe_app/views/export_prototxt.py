from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import yaml
from datetime import datetime
import random
import string
import sys
import os
from ide.utils.jsonToPrototxt import json_to_prototxt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


@csrf_exempt
def export_to_caffe(request):
    # Note : Remove the views for export by adding unittest for celery tasks
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        net_name = request.POST.get('net_name')
        if net_name == '':
            net_name = 'Net'
        try:
            prototxt, input_dim = json_to_prototxt(net, net_name)
            randomId = datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
            with open(BASE_DIR+'/media/'+randomId+'.prototxt', 'w') as f:
                f.write(prototxt)
            return JsonResponse({'result': 'success', 'id': randomId,
                                'name': randomId+'.prototxt', 'url': '/media/'+randomId+'.prototxt'})
        except:
            return JsonResponse({'result': 'error', 'error': str(sys.exc_info()[1])})
