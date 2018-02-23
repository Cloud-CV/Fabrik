import tensorflow as tf
from google.protobuf import text_format
from tensorflow.core.framework import graph_pb2
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import math
import re
import urllib2
from urlparse import urlparse

# map from operation name(tensorflow) to layer name(caffe)
op_layer_map = {'Placeholder': 'Input', 'Conv2D': 'Convolution', 'MaxPool': 'Pooling',
                'MatMul': 'InnerProduct', 'Relu': 'ReLU', 'Softmax': 'Softmax', 'LRN': 'LRN',
                'Concat': 'Concat', 'AvgPool': 'Pooling', 'Reshape': 'Flatten',
                'LeakyRelu': 'ReLU', 'Elu': 'ELU', 'Softsign': 'Softsign',
                'Softplus': 'Softplus'}
name_map = {'flatten': 'Flatten', 'dropout': 'Dropout',
            'batch': 'BatchNorm', 'add': 'Eltwise', 'mul': 'Eltwise'}


def get_layer_name(node_name):
    i = node_name.find('/')
    if i == -1:
        name = str(node_name)
    else:
        name = str(node_name[:i])
    return name


def get_layer_type(node_name):
    i = node_name.find('_')
    if i == -1:
        name = str(node_name)
    else:
        name = str(node_name[:i])
    return name


def get_padding(node, layer):
    layer_name = get_layer_name(node.name)
    input_shape = None
    output_shape = None
    for input_tensor in node.inputs:
        if get_layer_name(input_tensor.op.name) != layer_name:
            input_shape = input_tensor.get_shape()
    for output_tensor in node.outputs:
        output_shape = output_tensor.get_shape()

    '''
    Use this link: https://www.tensorflow.org/versions/r0.10/api_docs/python/nn.html
    pad_along_height = ((out_height - 1) * strides[1] +
                    filter_height - in_height)
    pad_along_width = ((out_width - 1) * strides[2] +
                       filter_width - in_width)
    pad_top = pad_along_height / 2
    pad_left = pad_along_width / 2
    '''

    pad_h = ((int(output_shape[1]) - 1) * layer['params']['stride_h'] +
             layer['params']['kernel_h'] - int(input_shape[1])) / float(2)
    pad_w = ((int(output_shape[2]) - 1) * layer['params']['stride_w'] +
             layer['params']['kernel_w'] - int(input_shape[2])) / float(2)

    # check this logic (see caffe-tensorflow/kaffe/shapes.py)
    if node.type == "Conv2D":
        pad_h = math.ceil(pad_h)
        pad_w = math.ceil(pad_w)
    elif node.type == "MaxPool" or node.type == "AvgPool":
        pad_h = math.floor(pad_h)
        pad_w = math.floor(pad_w)

    return int(pad_h), int(pad_w)


@csrf_exempt
def import_graph_def(request):
    if request.method == 'POST':
        if ('file' in request.FILES) and \
           (request.FILES['file'].content_type == 'application/octet-stream' or
                request.FILES['file'].content_type == 'text/plain'):
            try:
                f = request.FILES['file']
                config = f.read()
            except Exception:
                return JsonResponse({'result': 'error', 'error': 'No GraphDef model file found'})
        elif 'config' in request.POST:
            config = request.POST['config']
        elif 'url' in request.POST:
            try:
                url = urlparse(request.POST['url'])
                if url.netloc == 'github.com':
                    url = url._replace(netloc='raw.githubusercontent.com')
                    url = url._replace(path=url.path.replace('blob/', ''))
                config = urllib2.urlopen(url.geturl()).read()
            except Exception as ex:
                return JsonResponse({'result': 'error', 'error': 'Invalid URL\n'+str(ex)})
        else:
            return JsonResponse({'result': 'error', 'error': 'No GraphDef model found'})

        tf.reset_default_graph()
        graph_def = graph_pb2.GraphDef()
        d = {}
        order = []

        try:
            text_format.Merge(config, graph_def)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid GraphDef'})

        tf.import_graph_def(graph_def, name='')
        graph = tf.get_default_graph()

        for node in graph.get_operations():
            name = get_layer_name(node.name)
            if node.type == 'NoOp':
                continue
            if name not in d:
                d[name] = {'type': [], 'input': [], 'output': [], 'params': {}}
                order.append(name)
            if node.type in op_layer_map:
                d[name]['type'].append(op_layer_map[node.type])
            else:  # For cases where the ops are composed of only basic ops
                layer_type = get_layer_type(node.name)
                if layer_type in name_map:
                    if name_map[layer_type] not in d[name]['type']:
                        d[name]['type'].append(name_map[layer_type])
            for input_tensor in node.inputs:
                input_layer_name = get_layer_name(input_tensor.op.name)
                if input_layer_name != name:
                    d[name]['input'].append(input_layer_name)
                    if name not in d[input_layer_name]['output']:
                        d[input_layer_name]['output'].append(name)

        # seperating relu layers
        # This logic is only needed for inplace operations, it might be possible to do this
        # in a better way
        temp_d = {}
        for layer_name in d:
            if 'ReLU' in d[layer_name]['type'] and get_layer_type(layer_name) != 'activation':
                relu_layer_name = layer_name + '_relu'
                temp_d[relu_layer_name] = {'type': ['ReLU'], 'input': [layer_name],
                                           'output': d[layer_name]['output'], 'params': {}}
                for output_layer_name in d[layer_name]['output']:
                    for n, i in enumerate(d[output_layer_name]['input']):
                        if i == layer_name:
                            d[output_layer_name]['input'][n] = relu_layer_name
                d[layer_name]['output'] = [relu_layer_name]
        for key in temp_d:
            d[key] = temp_d[key]

        # setting params
        for node in graph.get_operations():
            if node.type == 'NoOp':
                continue
            name = get_layer_name(node.name)
            layer = d[name]
            if layer['type'][0] == 'Input':
                # NHWC data format
                layer['params']['dim'] = str(map(int, [node.get_attr('shape').dim[i].size
                                                       for i in [0, 1, 2, 3]]))[1:-1]

            elif layer['type'][0] == 'Convolution':
                if str(node.name) == name + '/weights' or str(node.name) == name + '/kernel':
                    # since conv takes weights as input, this node will be processed first
                    # acquired parameters are then required in get_padding function
                    layer['params']['kernel_h'] = int(
                        node.get_attr('shape').dim[0].size)
                    layer['params']['kernel_w'] = int(
                        node.get_attr('shape').dim[1].size)
                    layer['params']['num_output'] = int(
                        node.get_attr('shape').dim[3].size)
                if str(node.type) == 'Conv2D':
                    layer['params']['stride_h'] = int(
                        node.get_attr('strides')[1])
                    layer['params']['stride_w'] = int(
                        node.get_attr('strides')[2])
                    layer['params']['layer_type'] = '2D'
                    try:
                        layer['params']['pad_h'], layer['params']['pad_w'] = \
                            get_padding(node, layer)
                    except TypeError:
                        return JsonResponse({'result': 'error', 'error':
                                             'Missing shape info in GraphDef'})

            elif layer['type'][0] == 'Pooling':
                if str(node.type) == 'MaxPool':
                    layer['params']['pool'] = 0
                    layer['params']['kernel_h'] = int(
                        node.get_attr('ksize')[1])
                    layer['params']['kernel_w'] = int(
                        node.get_attr('ksize')[2])
                    layer['params']['stride_h'] = int(
                        node.get_attr('strides')[1])
                    layer['params']['stride_w'] = int(
                        node.get_attr('strides')[2])
                    layer['params']['layer_type'] = '2D'
                    try:
                        layer['params']['pad_h'], layer['params']['pad_w'] = \
                            get_padding(node, layer)
                    except TypeError:
                        return JsonResponse({'result': 'error', 'error':
                                             'Missing shape info in GraphDef'})

                if str(node.type) == 'AvgPool':
                    layer['params']['pool'] = 1
                    layer['params']['kernel_h'] = int(
                        node.get_attr('ksize')[1])
                    layer['params']['kernel_w'] = int(
                        node.get_attr('ksize')[2])
                    layer['params']['stride_h'] = int(
                        node.get_attr('strides')[1])
                    layer['params']['stride_w'] = int(
                        node.get_attr('strides')[2])
                    layer['params']['layer_type'] = '2D'
                    try:
                        layer['params']['pad_h'], layer['params']['pad_w'] = \
                            get_padding(node, layer)
                    except TypeError:
                        return JsonResponse({'result': 'error',
                                             'error': 'Missing shape info in GraphDef'})

            elif layer['type'][0] == 'InnerProduct':
                if str(node.name) == name + '/weights' or str(node.name) == name + '/kernel':
                    layer['params']['num_output'] = int(
                        node.get_attr('shape').dim[1].size)

            elif layer['type'][0] == 'BatchNorm':
                if re.match('.*\/batchnorm[_]?[0-9]?\/add.*', str(node.name)):
                    try:
                        layer['params']['eps'] = node.get_attr(
                            'value').float_val[0]
                    except:
                        pass

                if str(node.name) == name + '/AssignMovingAvg/decay':
                    layer['params']['moving_average_fraction'] = node.get_attr(
                        'value').float_val[0]

            elif layer['type'][0] == 'Eltwise':
                if str(node.name).split('_')[0] == 'add':
                    layer['params']['layer_type'] = 'Sum'
                if str(node.name).split('_')[0] == 'mul':
                    layer['params']['layer_type'] = 'Product'
                if str(node.name).split('_')[0] == 'dot':
                    layer['params']['layer_type'] = 'Dot'

            elif layer['type'][0] == 'ReLU':
                # if layer is a LeakyReLU layer
                if 'alpha' in node.node_def.attr:
                    layer['params']['negative_slope'] = node.get_attr('alpha')

            elif layer['type'][0] == 'ELU':
                # default value as tf.nn.elu layer computes exp(feature)-1 if < 0
                layer['params']['alpha'] = 1

            elif layer['type'][0] == 'Softplus':
                pass

            elif layer['type'][0] == 'Softsign':
                pass

            elif layer['type'][0] == 'Concat':
                if 'axis' in node.node_def.attr:
                    layer['params']['axis'] = node.get_attr('axis')

            elif layer['type'][0] == 'LRN':
                if ('alpha' in node.node_def.attr):
                    layer['params']['alpha'] = node.get_attr('alpha')
                if ('beta' in node.node_def.attr):
                    layer['params']['beta'] = node.get_attr('beta')
                if ('local_size' in node.node_def.attr):
                    layer['params']['local_size'] = node.get_attr('depth_radius')
                if ('bias' in node.node_def.attr):
                    layer['params']['k'] = node.get_attr('bias')

            elif layer['type'][0] == 'Softmax':
                pass

            elif layer['type'][0] == 'Flatten':
                pass

            elif layer['type'][0] == 'Dropout':
                if ('rate' in node.node_def.attr):
                    layer['params']['rate'] = node.get_attr('rate')
                if ('seed' in node.node_def.attr):
                    layer['params']['seed'] = node.get_attr('seed')
                if ('training' in node.node_def.attr):
                    layer['params']['trainable'] = node.get_attr('training')
        net = {}
        batch_norms = []
        for key in d.keys():
            if d[key]['type'][0] == 'BatchNorm' and len(d[key]['input']) > 0 and len(d[key]['output']) > 0:
                batch_norms.append(key)

        temp_d_batch = {}
        for layer_name in batch_norms:
            scale_layer_name = layer_name + '_scale'
            temp_d_batch[scale_layer_name] = {'type': ['Scale'], 'input': [layer_name],
                                              'output': d[layer_name]['output'], 'params': {}}
            for output_layer_name in d[layer_name]['output']:
                for n, i in enumerate(d[output_layer_name]['input']):
                    if i == layer_name:
                        d[output_layer_name]['input'][n] = scale_layer_name
            d[layer_name]['output'] = [scale_layer_name]
        for key in temp_d_batch:
            d[key] = temp_d_batch[key]

        for key in d.keys():
            net[key] = {
                'info': {
                    'type': d[key]['type'][0],
                    'phase': None
                },
                'connection': {
                    'input': d[key]['input'],
                    'output': d[key]['output']
                },
                'params': d[key]['params']
            }

        return JsonResponse({'result': 'success', 'net': net, 'net_name': ''})
