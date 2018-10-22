import os
import string
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from keras_app.views.export_json import export_json

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


@csrf_exempt
def export_to_tensorflow(request):
    # Note : Remove the views for export by adding unittest for celery tasks
    response = export_json(request, is_tf=True)
    if isinstance(response, JsonResponse):
        return response
    randomId = response['randomId']
    customLayers = response['customLayers']
    os.chdir(BASE_DIR + '/tensorflow_app/views/')
    os.system('KERAS_BACKEND=tensorflow python json2pbtxt.py -input_file ' +
              randomId + '.json -output_file ' + randomId)
    return JsonResponse({'result': 'success',
                         'id': randomId,
                         'name': randomId + '.pbtxt',
                         'url': '/media/' + randomId + '.pbtxt',
                         'customLayers': customLayers})
