import json
import os
import random
import string
import sys
import yaml

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ide.utils.shapes import get_shapes
from keras.models import Model
from layers_export import data, convolution, deconvolution, pooling, dense, dropout, embed,\
    recurrent, batchNorm, activation, flatten, reshape, eltwise, concat
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


@csrf_exempt
def exportJson(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        net_name = request.POST.get('net_name')
        if net_name == '':
            net_name = 'Net'
        try:
            net = get_shapes(net)
        except:
            return JsonResponse({'result': 'error', 'error': str(sys.exc_info()[1])})

        layer_map = {
            'ImageData': data,
            'Data': data,
            'Input': data,
            'WindowData': data,
            'MemoryData': data,
            'DummyData': data,
            'Convolution': convolution,
            'Pooling': pooling,
            'Deconvolution': deconvolution,
            'RNN': recurrent,
            'LSTM': recurrent,
            'InnerProduct': dense,
            'Dropout': dropout,
            'Embed': embed,
            'Concat': concat,
            'Eltwise': eltwise,
            'BatchNorm': batchNorm,
            'ReLU': activation,
            'PReLU': activation,
            'ELU': activation,
            'Sigmoid': activation,
            'TanH': activation,
            'Flatten': flatten,
            'Reshape': reshape,
            'Softmax': activation,
            'Scale': ''
        }

        stack = []
        net_out = {}
        dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData',
                      'MemoryData', 'DummyData']
        processedLayer = {}
        inputLayerId = None
        outputLayerId = None

        def isProcessPossible(layerId):
            inputs = net[layerId]['connection']['input']
            for layerId in inputs:
                if processedLayer[layerId] is False:
                    return False
            return True

        # Finding the data layer
        for layerId in net:
            processedLayer[layerId] = False
            if (net[layerId]['info']['type'] == 'Python'):
                return JsonResponse({'result': 'error', 'error': 'Cannot convert Python to Keras'})
            if(net[layerId]['info']['type'] in dataLayers):
                stack.append(layerId)
            if (not net[layerId]['connection']['input']):
                inputLayerId = layerId
            if (not net[layerId]['connection']['output']):
                outputLayerId = layerId

        while(len(stack)):
            if ('Loss' in net[layerId]['info']['type'] or
                    net[layerId]['info']['type'] == 'Accuracy'):
                pass
            elif (net[layerId]['info']['type'] in layer_map):
                i = len(stack) - 1
                while isProcessPossible(stack[i]) is False:
                    i = i - 1

                layerId = stack[i]
                stack.remove(layerId)
                if (net[layerId]['info']['type'] != 'Scale'):
                    layer_in = [net_out[inputId] for inputId in net[layerId]['connection']['input']]
                # Need to check if next layer is Scale
                if (net[layerId]['info']['type'] == 'BatchNorm'):
                    idNext = net[layerId]['connection']['output'][0]
                    nextLayer = net[idNext]
                    # If the BN layer is followed by Scale, then we need to pass both layers
                    # as in Keras parameters from both go into one single layer
                    net_out.update(layer_map[net[layerId]['info']['type']](net[layerId], layer_in,
                                                                           layerId, idNext,
                                                                           nextLayer))
                elif (net[layerId]['info']['type'] == 'Scale'):
                    type = net[net[layerId]['connection']['input'][0]]['info']['type']
                    if (type != 'BatchNorm'):
                        return JsonResponse({'result': 'error', 'error': 'Cannot convert ' +
                                            net[layerId]['info']['type'] + ' to Keras'})
                else:
                    net_out.update(layer_map[net[layerId]['info']['type']](net[layerId],
                                                                           layer_in, layerId))
                for outputId in net[layerId]['connection']['output']:
                    if outputId not in stack:
                        stack.append(outputId)
                processedLayer[layerId] = True
            else:
                return JsonResponse({'result': 'error', 'error': 'Cannot convert ' +
                                     net[layerId]['info']['type'] + ' to Keras'})

        model = Model(net_out[inputLayerId], net_out[outputLayerId], name=net_name)
        json_string = Model.to_json(model)
        randomId = datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
        with open(BASE_DIR+'/media/'+randomId+'.json', 'w') as f:
            json.dump(json.loads(json_string), f, indent=4)
        return JsonResponse({'result': 'success', 'id': randomId, 'name': randomId+'.json',
                             'url': '/media/'+randomId+'.json'})
