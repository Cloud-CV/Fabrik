import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from layers_import import Input, Convolution, Deconvolution, Pooling, Dense, Dropout, Embed,\
    Recurrent, BatchNorm, Activation, LeakyReLU, PReLU, ELU, Scale, Flatten, Reshape, Concat, \
    Eltwise, Padding, Upsample, LocallyConnected, ThresholdedReLU, Permute, RepeatVector,\
    ActivityRegularization, Masking, GaussianNoise, GaussianDropout, AlphaDropout
from keras.models import model_from_json, Sequential


@csrf_exempt
def import_json(request):
    if request.method == 'POST':
        if ('file' in request.FILES):
            try:
                f = request.FILES['file']
            except Exception:
                return JsonResponse({'result': 'error', 'error': 'No JSON model file found'})
        elif 'sample_id' in request.POST:
                try:
                    f = open(os.path.join(settings.BASE_DIR,
                                          'example', 'keras',
                                          request.POST['sample_id'] + '.json'), 'r')
                except Exception:
                    return JsonResponse({'result': 'error',
                                         'error': 'No JSON model file found'})
        try:
            model = json.load(f)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid JSON'})

    model = model_from_json(json.dumps(model))
    layer_map = {
        'InputLayer': Input,
        'Dense': Dense,
        'Activation': Activation,
        'softmax': Activation,
        'selu': Activation,
        'softplus': Activation,
        'softsign': Activation,
        'relu': Activation,
        'tanh': Activation,
        'sigmoid': Activation,
        'hard_sigmoid': Activation,
        'Dropout': Dropout,
        'Flatten': Flatten,
        'Reshape': Reshape,
        'Permute': Permute,
        'RepeatVector': RepeatVector,
        'ActivityRegularization': ActivityRegularization,
        'Masking': Masking,
        'Conv1D': Convolution,
        'Conv2D': Convolution,
        'Conv2DTranspose': Deconvolution,
        'Conv3D': Convolution,
        'UpSampling1D': Upsample,
        'UpSampling2D': Upsample,
        'UpSampling3D': Upsample,
        'ZeroPadding1D': Padding,
        'ZeroPadding2D': Padding,
        'ZeroPadding3D': Padding,
        'MaxPooling1D': Pooling,
        'MaxPooling2D': Pooling,
        'MaxPooling3D': Pooling,
        'AveragePooling1D': Pooling,
        'AveragePooling2D': Pooling,
        'AveragePooling3D': Pooling,
        'GlobalMaxPooling1D': Pooling,
        'GlobalAveragePooling1D': Pooling,
        'GlobalMaxPooling2D': Pooling,
        'GlobalAveragePooling2D': Pooling,
        'LocallyConnected1D': LocallyConnected,
        'LocallyConnected2D': LocallyConnected,
        'SimpleRNN': Recurrent,
        'GRU': Recurrent,
        'LSTM': Recurrent,
        'Embedding': Embed,
        'Add': Eltwise,
        'Multiply': Eltwise,
        'Average': Eltwise,
        'Maximum': Eltwise,
        'Concatenate': Concat,
        'Dot': Eltwise,
        'LeakyReLU': LeakyReLU,
        'PReLU': PReLU,
        'elu': ELU,
        'ELU': ELU,
        'ThresholdedReLU': ThresholdedReLU,
        'BatchNormalization': BatchNorm,
        'GaussianNoise': GaussianNoise,
        'GaussianDropout': GaussianDropout,
        'AlphaDropout': AlphaDropout
    }

    hasActivation = ['Conv1D', 'Conv2D', 'Conv3D', 'Conv2DTranspose', 'Dense', 'LocallyConnected1D',
                     'LocallyConnected2D', 'SeparableConv2D', 'LSTM', 'SimpleRNN', 'GRU']

    net = {}
    # Add dummy input layer if sequential model
    if (isinstance(model, Sequential)):
        input_layer = model.layers[0].inbound_nodes[0].inbound_layers[0]
        # If embedding is the first layer, the input has shape (None, None)
        if (model.layers[0].__class__.__name__ == 'Embedding'):
            input_layer.batch_input_shape = (None, model.layers[0].input_dim)
        net[input_layer.name] = Input(input_layer)
    for idx, layer in enumerate(model.layers):
        name = ''
        class_name = layer.__class__.__name__
        if (class_name in layer_map):
            # This extra logic is to handle connections if the layer has an Activation
            if (class_name in hasActivation and layer.activation.func_name != 'linear'):
                net[layer.name+class_name] = layer_map[class_name](layer)
                net[layer.name] = layer_map[layer.activation.func_name](layer)
                net[layer.name+class_name]['connection']['output'].append(layer.name)
                name = layer.name+class_name
            # To check if a Scale layer is required
            elif (class_name == 'BatchNormalization' and (
                    layer.center or layer.scale)):
                net[layer.name+class_name] = layer_map[class_name](layer)
                net[layer.name] = Scale(layer)
                net[layer.name+class_name]['connection']['output'].append(layer.name)
                name = layer.name+class_name
            else:
                net[layer.name] = layer_map[class_name](layer)
                name = layer.name
            if (layer.inbound_nodes[0].inbound_layers):
                for node in layer.inbound_nodes[0].inbound_layers:
                    net[node.name]['connection']['output'].append(name)
        else:
            raise Exception('Cannot import layer of '+layer.__class__.__name__+' type')
    # collect names of all zeroPad layers
    zeroPad = []
    # Transfer parameters and connections from zero pad
    # The 'pad' param is a list with upto 3 elements
    for node in net:
        if (net[node]['info']['type'] == 'Pad'):
            net[net[node]['connection']['output'][0]]['connection']['input'] = \
                net[node]['connection']['input']
            net[net[node]['connection']['input'][0]]['connection']['output'] = \
                net[node]['connection']['output']
            net[net[node]['connection']['output'][0]]['params']['pad_w'] += \
                net[node]['params']['pad'][0]
            if (net[net[node]['connection']['output'][0]]['params']['layer_type'] == '2D'):
                net[net[node]['connection']['output'][0]]['params']['pad_h'] += \
                    net[node]['params']['pad'][1]
            elif (net[net[node]['connection']['output'][0]]['params']['layer_type'] == '3D'):
                net[net[node]['connection']['output'][0]]['params']['pad_h'] += \
                    net[node]['params']['pad'][1]
                net[net[node]['connection']['output'][0]]['params']['pad_d'] += \
                    net[node]['params']['pad'][2]
            zeroPad.append(node)
        # Switching connection order to handle visualization
        elif (net[node]['info']['type'] == 'Eltwise'):
            net[node]['connection']['input'] = net[node]['connection']['input'][::-1]
    for node in zeroPad:
        net.pop(node, None)
    return JsonResponse({'result': 'success', 'net': net, 'net_name': model.name})
