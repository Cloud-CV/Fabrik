import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from layers_import import Input, Convolution, Deconvolution, Pooling, Dense, Dropout, Embed,\
    Recurrent, BatchNorm, Activation, LeakyReLU, PReLU, Scale, Flatten, Reshape, Concat, Eltwise,\
    Padding
from keras.models import model_from_json, Sequential


@csrf_exempt
def importJson(request):
    if request.method == 'POST':
        try:
            f = request.FILES['file']
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'No JSON model file found'})

        try:
            model = json.load(f)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid JSON'})

    model = model_from_json(json.dumps(model))

    layer_map = {
        'InputLayer': Input,
        'Conv2D': Convolution,
        'Conv2DTranspose': Deconvolution,
        'MaxPooling2D': Pooling,
        'GlobalMaxPooling2D': Pooling,
        'AveragePooling2D': Pooling,
        'GlobalAveragePooling2D': Pooling,
        'Dense': Dense,
        'Dropout': Dropout,
        'Embedding': Embed,
        'SimpleRNN': Recurrent,
        'LSTM': Recurrent,
        'BatchNormalization': BatchNorm,
        'Activation': Activation,
        'relu': Activation,
        'softmax': Activation,
        'elu': Activation,
        'tanh': Activation,
        'sigmoid': Activation,
        'LeakyReLU': LeakyReLU,
        'PReLU': PReLU,
        'Flatten': Flatten,
        'Reshape': Reshape,
        'Concatenate': Concat,
        'Add': Eltwise,
        'Multiply': Eltwise,
        'Maximum': Eltwise,
        'ZeroPadding2D': Padding,
    }

    hasActivation = ['Conv2D', 'Conv2DTranspose', 'Dense']

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
    for node in net:
        if (net[node]['info']['type'] == 'Pad'):
            net[net[node]['connection']['output'][0]]['connection']['input'] = \
                net[node]['connection']['input']
            net[net[node]['connection']['output'][0]]['params']['pad_w'] += \
                net[node]['params']['pad_w']
            net[net[node]['connection']['output'][0]]['params']['pad_h'] += \
                net[node]['params']['pad_h']
            net[net[node]['connection']['input'][0]]['connection']['output'] = \
                net[node]['connection']['output']
            zeroPad.append(node)
        # Switching connection order to handle visualization
        elif (net[node]['info']['type'] == 'Eltwise'):
            net[node]['connection']['input'] = net[node]['connection']['input'][::-1]
    for node in zeroPad:
        net.pop(node, None)
    return JsonResponse({'result': 'success', 'net': net, 'net_name': model.name})
