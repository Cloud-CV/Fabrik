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
    recurrent, batch_norm, activation, flatten, reshape, eltwise, concat, upsample, locally_connected,\
    permute, repeat_vector, regularization, masking, gaussian_noise, gaussian_dropout, alpha_dropout
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


@csrf_exempt
def export_json(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        net_name = request.POST.get('net_name')
        if net_name == '':
            net_name = 'Net'
        try:
            net = get_shapes(net)
        except BaseException:
            return JsonResponse(
                {'result': 'error', 'error': str(sys.exc_info()[1])})

        layer_map = {
            'ImageData': data,
            'Data': data,
            'Input': data,
            'WindowData': data,
            'MemoryData': data,
            'DummyData': data,
            'InnerProduct': dense,
            'Softmax': activation,
            'SELU': activation,
            'Softplus': activation,
            'Softsign': activation,
            'ReLU': activation,
            'TanH': activation,
            'Sigmoid': activation,
            'HardSigmoid': activation,
            'Dropout': dropout,
            'Flatten': flatten,
            'Reshape': reshape,
            'Permute': permute,
            'RepeatVector': repeat_vector,
            'Regularization': regularization,
            'Masking': masking,
            'Convolution': convolution,
            'Deconvolution': deconvolution,
            'Upsample': upsample,
            'Pooling': pooling,
            'LocallyConnected': locally_connected,
            'RNN': recurrent,
            'GRU': recurrent,
            'LSTM': recurrent,
            'Embed': embed,
            'Concat': concat,
            'Eltwise': eltwise,
            'PReLU': activation,
            'ELU': activation,
            'ThresholdedReLU': activation,
            'BatchNorm': batch_norm,
            'GaussianNoise': gaussian_noise,
            'GaussianDropout': gaussian_dropout,
            'AlphaDropout': alpha_dropout,
            'Scale': ''
        }

        # Check if conversion is possible
        for layerId in net:
            layerType = net[layerId]['info']['type']
            if ('Loss' in layerType or layerType ==
                    'Accuracy' or layerType in layer_map):
                pass
            else:
                return JsonResponse(
                    {'result': 'error', 'error': 'Cannot convert ' + layerType + ' to Keras'})

        stack = []
        net_out = {}
        dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData',
                      'MemoryData', 'DummyData']
        processedLayer = {}
        inputLayerId = []
        outputLayerId = []

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
                return JsonResponse(
                    {'result': 'error', 'error': 'Cannot convert Python to Keras'})
            if(net[layerId]['info']['type'] in dataLayers):
                stack.append(layerId)
            if (not net[layerId]['connection']['input']):
                inputLayerId.append(layerId)
            if (not net[layerId]['connection']['output']):
                outputLayerId.append(layerId)

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
                    layer_in = [net_out[inputId]
                                for inputId in net[layerId]['connection']['input']]
                # Need to check if next layer is Scale
                if (net[layerId]['info']['type'] == 'BatchNorm'):
                    idNext = net[layerId]['connection']['output'][0]
                    nextLayer = net[idNext]
                    # If the BN layer is followed by Scale, then we need to pass both layers
                    # as in Keras parameters from both go into one single layer
                    net_out.update(layer_map[net[layerId]['info']['type']](
                        net[layerId], layer_in, layerId, idNext, nextLayer))
                elif (net[layerId]['info']['type'] == 'Scale'):
                    type = net[net[layerId]['connection']
                               ['input'][0]]['info']['type']
                    if (type != 'BatchNorm'):
                        return JsonResponse({'result': 'error', 'error': 'Cannot convert ' +
                                             net[layerId]['info']['type'] + ' to Keras'})
                else:
                    net_out.update(layer_map[net[layerId]['info']['type']](
                        net[layerId], layer_in, layerId))
                for outputId in net[layerId]['connection']['output']:
                    if outputId not in stack:
                        stack.append(outputId)
                processedLayer[layerId] = True
            else:
                return JsonResponse({'result': 'error', 'error': 'Cannot convert ' +
                                     net[layerId]['info']['type'] + ' to Keras'})

        final_input = []
        final_output = []
        for i in inputLayerId:
            final_input.append(net_out[i])

        for j in outputLayerId:
            final_output.append(net_out[j])

        model = Model(inputs=final_input, outputs=final_output, name=net_name)
        json_string = Model.to_json(model)
        randomId = datetime.now().strftime('%Y%m%d%H%M%S') + randomword(5)
        with open(BASE_DIR + '/media/' + randomId + '.json', 'w') as f:
            json.dump(json.loads(json_string), f, indent=4)
        return JsonResponse({'result': 'success',
                             'id': randomId,
                             'name': randomId + '.json',
                             'url': '/media/' + randomId + '.json'})
