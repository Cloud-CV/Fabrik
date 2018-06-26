import random
import string
import sys

from caffe_app.models import ModelExport
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from yaml import safe_load
from django.shortcuts import render


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def save_to_db(request):
    if request.method == 'POST':
        net = request.POST.get('net')
        net_name = request.POST.get('net_name')
        if net_name == '':
            net_name = 'Net'
        if request.POST.get('model_id', 'null') != 'null':
            model = ModelExport.objects.get(id=request.POST.get('model_id'))
            model.network = net
            model.updatedOn = datetime.now()
            model.name = net_name
            model.save()
            return JsonResponse({'result': 'success', 'id': request.POST.get('model_id'),
                                'user': request.user.is_authenticated()})
        else:
            try:
                random_id = datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
                if request.user.is_authenticated():
                    model = ModelExport(name=net_name, id=random_id, network=net, createdOn=datetime.now(),
                                        updatedOn=datetime.now(), user=request.user)
                else:
                    model = ModelExport(name=net_name, id=random_id, network=net, createdOn=datetime.now(),
                                        updatedOn=datetime.now())
                model.save()
                return JsonResponse({'result': 'success', 'id': random_id,
                                    'user': request.user.is_authenticated()})
            except:
                return JsonResponse({'result': 'error', 'error': str(sys.exc_info()[1])})


@csrf_exempt
def load_from_db(request):
    if request.method == 'POST':
        if 'proto_id' in request.POST:
            try:
                model = ModelExport.objects.get(pk=request.POST['proto_id'])
                net = safe_load(model.network)
            except Exception:
                return JsonResponse({'result': 'error',
                                     'error': 'No network file found'})
            return JsonResponse({'result': 'success', 'net': net, 'net_name': model.name})

    if request.method == 'GET':
        return index(request)
