import copy
import sys
import yaml

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.shapes import get_shapes, get_layer_shape, handle_concat_layer


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def fetch_layer_shape(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        layerId = request.POST.get('layerId')
        try:
            net[layerId]['shape'] = {}
            net[layerId]['shape']['input'] = None
            net[layerId]['shape']['output'] = None
            dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData']

            # Obtain input shape of new layer
            if (net[layerId]['info']['type'] == "Concat"):
                for parentLayerId in net[layerId]['connection']['input']:
                    # Check if parent layer have shapes
                    if (net[parentLayerId]['shape']['output']):
                        net[layerId]['shape']['input'] = handle_concat_layer(net[layerId], net[parentLayerId])
            elif (not (net[layerId]['info']['type'] in dataLayers)):
                if (len(net[layerId]['connection']['input']) > 0):
                    parentLayerId = net[layerId]['connection']['input'][0]
                    # Check if parent layer have shapes
                    if (net[parentLayerId]['shape']['output']):
                        net[layerId]['shape']['input'] = net[parentLayerId]['shape']['output'][:]

            # Obtain output shape of new layer
            if (net[layerId]['info']['type'] in dataLayers):
                # handling Data Layers separately
                if (len(net[layerId]['params']['dim'])):
                    net[layerId]['shape']['input'], net[layerId]['shape']['output'] =\
                            get_layer_shape(net[layerId])
            else:
                if (net[layerId]['shape']['input']):
                    net[layerId]['shape']['output'] = get_layer_shape(net[layerId])
        except BaseException:
            return JsonResponse({
                'result': 'error', 'error': str(sys.exc_info()[1])})
        return JsonResponse({'result': 'success', 'net': net})


@csrf_exempt
def calculate_parameter(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        try:
            # While calling get_shapes we need to remove the flag
            # added in frontend to show the parameter on pane
            netObj = copy.deepcopy(net)
            for layerId in netObj:
                for param in netObj[layerId]['params']:
                    netObj[layerId]['params'][param] = netObj[layerId]['params'][param][0]
            # use get_shapes method to obtain shapes of each layer
            netObj = get_shapes(netObj)
            for layerId in net:
                net[layerId]['shape'] = {}
                net[layerId]['shape']['input'] = netObj[layerId]['shape']['input']
                net[layerId]['shape']['output'] = netObj[layerId]['shape']['output']
        except BaseException:
            return JsonResponse({
                'result': 'error', 'error': str(sys.exc_info()[1])})
        return JsonResponse({'result': 'success', 'net': net})
