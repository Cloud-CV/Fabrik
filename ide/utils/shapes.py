import numpy as np


def data(layer):
    Input = []
    if (layer['info']['type'] in ['ImageData', 'Data', 'WindowData']):
        if ('crop_size' in layer['params']):
            Output = [3] + [layer['params']['crop_size']]*2
        elif ('new_height' in layer['params'] and 'new_width' in layer['params']):
            Output = [3, layer['params']['new_height'], layer['params']['new_width']]
    elif (layer['info']['type'] in ['Input', 'DummyData']):
        Output = map(int, layer['params']['dim'].split(','))[1:]
    elif (layer['info']['type'] == 'MemoryData'):
        Output = [3, layer['params']['height'], layer['params']['width']]
    else:
        raise Exception('Cannot determine shape of ' + layer['info']['type'] + 'layer.')
    return Input, Output


def identity(layer):
    return layer['shape']['input']


def filter(layer):
    _, i_h, i_w = layer['shape']['input']
    k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
    s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
    p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
    if (layer['info']['type'] == 'Deconvolution'):
        o_h = int((i_h - 1)*s_h + k_h - 2*p_h)
        o_w = int((i_w - 1)*s_w + k_w - 2*p_w)
    else:
        o_h = int((i_h + 2 * p_h - k_h) / float(s_h) + 1)
        o_w = int((i_w + 2 * p_w - k_w) / float(s_w) + 1)
    if (layer['info']['type'] == 'Pooling'):
        num_out = layer['shape']['input'][0]
    else:
        num_out = layer['params']['num_output']
    return [num_out, o_h, o_w]


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
    return temp.shape


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
                    stack.append(layerId)
            else:
                if (net[layerId]['params']['endPoint'] == "1, 0"):
                    stack.append(layerId)
        if(net[layerId]['info']['type'] in dataLayers):
            stack.append(layerId)

    while(len(stack)):
        layerId = stack[0]
        stack.remove(layerId)

        if(net[layerId]['info']['type'] in dataLayers):
            net[layerId]['shape']['input'], net[layerId]['shape']['output'] = data(net[layerId])

        elif(net[layerId]['info']['type'] in ['Convolution', 'Pooling', 'Deconvolution']):
            net[layerId]['shape']['output'] = filter(net[layerId])

        elif(net[layerId]['info']['type'] in ['InnerProduct', 'Recurrent', 'RNN', 'LSTM', 'Embed']):
            net[layerId]['shape']['output'] = output(net[layerId])

        elif(net[layerId]['info']['type'] == 'Flatten'):
            net[layerId]['shape']['output'] = flatten(net[layerId])

        elif(net[layerId]['info']['type'] == 'Reshape'):
            net[layerId]['shape']['output'] = reshape(net[layerId])

        elif(net[layerId]['info']['type'] in ['SPP', 'Crop']):
            raise Exception('Cannot determine shape of ' + net[layerId]['info']['type'] + 'layer.')

        else:
            net[layerId]['shape']['output'] = identity(net[layerId])

        for outputId in net[layerId]['connection']['output']:
            if (not processedLayer[outputId]):
                net[outputId]['shape']['input'] = net[layerId]['shape']['output']
                stack.append(outputId)

        processedLayer[layerId] = True

    return net
