import json
import os
import random
import string
import yaml
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from keras.models import Model
from layers_export import data, convolution, deconvolution, pooling, dense, dropout, embed,\
    recurrent, batch_norm, activation, flatten, reshape, eltwise, concat, upsample, locally_connected,\
    permute, repeat_vector, regularization, masking, gaussian_noise, gaussian_dropout, alpha_dropout, \
    bidirectional, time_distributed, lrn, depthwiseConv
from ..custom_layers import config as custom_layers_config


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


@csrf_exempt
def export_json(request, is_tf=False):
    # Note : Remove the views for export by adding unittest for celery tasks
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        net_name = request.POST.get('net_name')
        if net_name == '':
            net_name = 'Net'

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
            'Linear': activation,
            'Dropout': dropout,
            'Flatten': flatten,
            'Reshape': reshape,
            'Permute': permute,
            'RepeatVector': repeat_vector,
            'Regularization': regularization,
            'Masking': masking,
            'Convolution': convolution,
            'Deconvolution': deconvolution,
            'DepthwiseConv': depthwiseConv,
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
            'Scale': '',
            'TimeDistributed': time_distributed,
            'Bidirectional': bidirectional
        }

        custom_layers_map = {
            'LRN': lrn
        }

        # Remove any duplicate activation layers (timedistributed and bidirectional layers)
        redundant_layers = []
        for layerId in net:
            if (net[layerId]['connection']['input']
                    and net[net[layerId]['connection']['input'][0]]['info']['type'] in
                    ['TimeDistributed', 'Bidirectional']):
                if len(net[layerId]['connection']['output']) > 0:
                    target = net[layerId]['connection']['output'][0]
                    outputs = net[target]['connection']['output']
                    if len(outputs) > 0:
                        net[layerId]['connection']['output'] = outputs
                        for j in outputs:
                            net[j]['connection']['input'] = [
                                x if (x != target) else layerId for x in net[j]['connection']['input']]
                        redundant_layers.append(target)
            elif (net[layerId]['info']['type'] == 'Input'
                  and net[net[layerId]['connection']['output'][0]]['info']['type'] in
                  ['TimeDistributed', 'Bidirectional']):
                connected_layer = net[layerId]['connection']['output'][0]
                net[connected_layer]['params']['batch_input_shape'] = net[layerId]['params']['dim']
        for i in redundant_layers:
            del net[i]

        # Check if conversion is possible
        error = []
        custom_layers = []
        for key, value in custom_layers_map.iteritems():
            layer_map[key] = value
        for layerId in net:
            layerType = net[layerId]['info']['type']
            if (layerType in custom_layers_map):
                custom_layers.append(layerType)
            if ('Loss' in layerType or layerType ==
                    'Accuracy' or layerType in layer_map):
                pass
            else:
                error.append(layerId + '(' + layerType + ')')
        if len(error):
            return JsonResponse(
                {'result': 'error', 'error': 'Cannot convert ' + ', '.join(error) + ' to Keras'})

        stack = []
        net_out = {}
        dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData',
                      'MemoryData', 'DummyData', 'Bidirectional',
                      'TimeDistributed']
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
                error.append(layerId + '(Python)')
                continue
            if(net[layerId]['info']['type'] in dataLayers):
                stack.append(layerId)
            if (not net[layerId]['connection']['input']):
                inputLayerId.append(layerId)
            if (not net[layerId]['connection']['output']):
                outputLayerId.append(layerId)
        if len(error):
            return JsonResponse(
                {'result': 'error', 'error': 'Cannot convert ' + ', '.join(error) + ' to Keras'})

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
                elif (net[layerId]['info']['type'] in ['TimeDistributed', 'Bidirectional']):
                    idNext = net[layerId]['connection']['output'][0]
                    net_out.update(
                        layer_map[net[layerId]['info']['type']](layerId, idNext, net, layer_in, layer_map))
                    if len(net[idNext]['connection']['output']) > 0:
                        net[net[idNext]['connection']['output'][0]
                            ]['connection']['input'] = [layerId]
                    processedLayer[idNext] = True
                    processedLayer[layerId] = True
                else:
                    net_out.update(layer_map[net[layerId]['info']['type']](
                        net[layerId], layer_in, layerId))
                for outputId in net[layerId]['connection']['output']:
                    if outputId not in stack:
                        stack.append(outputId)
                processedLayer[layerId] = True
            else:
                error.append(
                    layerId + '(' + net[layerId]['info']['type'] + ')')
        if len(error):
            return JsonResponse(
                {'result': 'error', 'error': 'Cannot convert ' + ', '.join(error) + ' to Keras'})

        final_input = []
        final_output = []
        for i in inputLayerId:
            final_input.append(net_out[i])

        for j in outputLayerId:
            if (net[net[j]['connection']['input'][0]]['info']['type'] in
                    ['TimeDistributed', 'Bidirectional']):
                final_output.append(net_out[net[j]['connection']['input'][0]])
            else:
                final_output.append(net_out[j])

        model = Model(inputs=final_input, outputs=final_output, name=net_name)
        json_string = Model.to_json(model)

        randomId = datetime.now().strftime('%Y%m%d%H%M%S') + randomword(5)
        with open(BASE_DIR + '/media/' + randomId + '.json', 'w') as f:
            json.dump(json.loads(json_string), f, indent=4)

        custom_layers_response = []
        for layer in set(custom_layers):
            layer_data = {'name': layer}
            layer_data.update(custom_layers_config.config[layer])
            custom_layers_response.append(layer_data)

        if not is_tf:
            return JsonResponse({'result': 'success',
                                 'id': randomId,
                                 'name': randomId + '.json',
                                 'url': '/media/' + randomId + '.json',
                                 'customLayers': custom_layers_response
                                 })
        else:
            return {'randomId': randomId, 'customLayers': custom_layers_response}
