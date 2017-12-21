import numpy as np


def data(layer):
    Input = []
    if (layer['info']['type'] in ['ImageData', 'Data', 'WindowData']):
        if (('crop_size' in layer['params']) and (layer['params']['crop_size'] != 0)):
            Output = [3] + [layer['params']['crop_size']]*2
        elif (('new_height' in layer['params']) and ('new_width' in layer['params'])):
            Output = [3, layer['params']['new_height'], layer['params']['new_width']]
    elif (layer['info']['type'] in ['Input', 'DummyData']):
        Output = map(int, layer['params']['dim'].split(','))[1:]
    elif (layer['info']['type'] == 'MemoryData'):
        Output = [3, layer['params']['height'], layer['params']['width']]
    else:
        raise Exception('Cannot determine shape of ' + layer['info']['type'] + ' layer.')
    return Input, Output


def identity(layer):
    return layer['shape']['input']


def filter(layer):
    if (layer['info']['type'] == 'Pooling'):
        num_out = layer['shape']['input'][0]
    else:
        num_out = layer['params']['num_output']
    if (layer['info']['type'] in ['Deconvolution', 'DepthwiseConv']):
        _, i_h, i_w = layer['shape']['input']
        k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
        s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
        p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
        o_h = int((i_h - 1)*s_h + k_h - 2*p_h)
        o_w = int((i_w - 1)*s_w + k_w - 2*p_w)
        return [num_out, o_h, o_w]
    else:
        if (layer['params']['layer_type'] == '1D'):
            _, i_w = layer['shape']['input']
            k_w = layer['params']['kernel_w']
            s_w = layer['params']['stride_w']
            p_w = layer['params']['pad_w']
            o_w = int((i_w + 2 * p_w - k_w) / float(s_w) + 1)
            return [num_out, o_w]
        elif (layer['params']['layer_type'] == '2D'):
            _, i_h, i_w = layer['shape']['input']
            k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
            s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
            p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
            o_h = int((i_h + 2 * p_h - k_h) / float(s_h) + 1)
            o_w = int((i_w + 2 * p_w - k_w) / float(s_w) + 1)
            return [num_out, o_h, o_w]
        else:
            _, i_d, i_h, i_w = layer['shape']['input']
            k_h, k_w, k_d = layer['params']['kernel_h'], layer['params']['kernel_w'],\
                layer['params']['kernel_d']
            s_h, s_w, s_d = layer['params']['stride_h'], layer['params']['stride_w'],\
                layer['params']['stride_d']
            p_h, p_w, p_d = layer['params']['pad_h'], layer['params']['pad_w'],\
                layer['params']['pad_d']
            o_h = int((i_h + 2 * p_h - k_h) / float(s_h) + 1)
            o_w = int((i_w + 2 * p_w - k_w) / float(s_w) + 1)
            o_d = int((i_d + 2 * p_d - k_d) / float(s_d) + 1)
            return [num_out, o_d, o_h, o_w]


def upsample(layer):
    if (layer['params']['layer_type'] == '1D'):
        num_out, i_w = layer['shape']['input']
        s_w = layer['params']['size_w']
        o_w = int(i_w*s_w)
        return [num_out, o_w]
    elif (layer['params']['layer_type'] == '2D'):
        num_out, i_h, i_w = layer['shape']['input']
        s_h, s_w = layer['params']['size_h'], layer['params']['size_w']
        o_w = int(i_w*s_w)
        o_h = int(i_h*s_h)
        return [num_out, o_h, o_w]
    else:
        num_out, i_h, i_w, i_d = layer['shape']['input']
        s_h, s_w, s_d = layer['params']['size_h'], layer['params']['size_w'],\
            layer['params']['size_d']
        o_w = int(i_w*s_w)
        o_h = int(i_h*s_h)
        o_d = int(i_d*s_d)
        return [num_out, o_h, o_w, o_d]


def output(layer):
    return [layer['params']['num_output']]


def flatten(layer):
    out = 1
    for i in layer['shape']['input']:
        out *= i
    return [out]


def reshape(layer):
    temp = np.zeros(layer['shape']['input'])
    shape = map(int, layer['params']['dim'].split(','))[1:]
    temp = np.reshape(temp, shape)
    return list(temp.shape[::-1])


def repeat(layer):
    shape = layer['shape']['input']
    shape = shape + [layer['params']['n']]
    return shape


def handle_concat_layer(outputLayer, inputLayer):
    if('input' not in outputLayer['shape']):
        shape = inputLayer['shape']['output'][:]
    else:
        old_num_output = outputLayer['shape']['input'][0]
        shape = inputLayer['shape']['output'][:]
        shape[0] += old_num_output
    return shape


def get_layer_shape(layerId, net):
    # separating checking the type of layer inorder to make it modular
    # which can be reused in case we only want to get shapes of a single
    # layer, for example: if a new layer is added to already drawn model
    dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData']

    if(net[layerId]['info']['type'] in dataLayers):
        return data(net[layerId])

    elif(net[layerId]['info']['type'] in ['Convolution', 'Pooling', 'Deconvolution', 'DepthwiseConv']):
        return filter(net[layerId])

    elif(net[layerId]['info']['type'] in ['InnerProduct', 'Recurrent', 'RNN', 'LSTM', 'Embed']):
        return output(net[layerId])

    elif(net[layerId]['info']['type'] == 'Flatten'):
        return flatten(net[layerId])

    elif(net[layerId]['info']['type'] == 'Reshape'):
        return reshape(net[layerId])

    elif(net[layerId]['info']['type'] == 'Upsample'):
        return upsample(net[layerId])

    elif(net[layerId]['info']['type'] == 'RepeatVector'):
        return repeat(net[layerId])

    elif(net[layerId]['info']['type'] in ['SPP', 'Crop']):
        raise Exception('Cannot determine shape of ' + net[layerId]['info']['type'] + 'layer.')

    else:
        return identity(net[layerId])


def get_shapes(net):
    stack = []
    dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData']
    processedLayer = {}

    # Finding the data layer
    for layerId in net:
        processedLayer[layerId] = False
        net[layerId]['shape'] = {}
        if (net[layerId]['info']['type'] == 'Python'):
            if ('endPoint' not in net[layerId]['params'].keys()):
                if (not net[layerId]['connection']['input']):
                    raise Exception('Cannot determine shape of Python layer.')
            else:
                if (net[layerId]['params']['endPoint'] == "1, 0"):
                    raise Exception('Cannot determine shape of Python layer.')
        if(net[layerId]['info']['type'] in dataLayers):
            stack.append(layerId)

    while(len(stack)):
        layerId = stack[0]
        stack.remove(layerId)

        if(net[layerId]['info']['type'] in dataLayers):
            net[layerId]['shape']['input'], net[layerId]['shape']['output'] = get_layer_shape(layerId, net)
        else:
            net[layerId]['shape']['output'] = get_layer_shape(layerId, net)

        for outputId in net[layerId]['connection']['output']:
            if (not processedLayer[outputId]):
                # Handling Concat layer separately
                if (net[outputId]['info']['type'] == "Concat"):
                    net[outputId]['shape']['input'] = handle_concat_layer(net[outputId], net[layerId])
                else:
                    net[outputId]['shape']['input'] = net[layerId]['shape']['output'][:]

                # Implement topo sort check
                flag = True
                for parentLayerId in net[outputId]['connection']['input']:
                    if ((not processedLayer[parentLayerId]) and parentLayerId != layerId):
                        flag = False
                        break
                if flag:
                    stack.append(outputId)
            else:
                if (net[outputId]['info']['type'] == "Concat"):
                    net[outputId]['shape']['input'] = handle_concat_layer(net[outputId], net[layerId])

        processedLayer[layerId] = True

    return net
