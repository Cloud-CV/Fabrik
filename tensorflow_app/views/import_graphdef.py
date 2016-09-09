import tensorflow as tf
from google.protobuf import text_format
from tensorflow.core.framework import graph_pb2
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import yaml
import math

# map from operation name(tensorflow) to layer name(caffe)
op_layer_map = { 'Placeholder':'Input','Conv2D':'Convolution','MaxPool':'Pooling','MatMul':'InnerProduct','Relu':'ReLU','Softmax':'Softmax','LRN':'LRN','Concat':'Concat','AvgPool':'Pooling'}

def get_layer_name(node_name):
    i = node_name.find('/')
    if i == -1:
        name = str(node_name)
    else:
        name = str(node_name[:i])
    return name

def get_padding(node,layer):
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

    pad_h = ((int(output_shape[1]) - 1) * layer['params']['stride_h'] + layer['params']['kernel_h'] - int(input_shape[1]))/float(2)
    pad_w = ((int(output_shape[2]) - 1) * layer['params']['stride_w'] + layer['params']['kernel_w'] - int(input_shape[2]))/float(2)

    # check this logic (see caffe-tensorflow/kaffe/shapes.py)
    if node.type == "Conv2D":
        pad_h = math.ceil(pad_h)
        pad_w = math.ceil(pad_w)
    elif node.type == "MaxPool" or node.type == "AvgPool":
        pad_h = math.floor(pad_h)
        pad_w = math.floor(pad_w)

    return int(pad_h),int(pad_w)

@csrf_exempt
def importGraphDef(request):
    if request.method == 'POST':
        try:
            f = request.FILES['file']
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'No GraphDef model file found'})

        graph_def = graph_pb2.GraphDef()
        d = {}
        order = []

        try:
            text_format.Merge(f.read(), graph_def)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid GraphDef'})

        tf.import_graph_def(graph_def,name='')
        graph = tf.get_default_graph()


        for node in graph.get_operations():
            name = get_layer_name(node.name)
            if name not in d:
                d[name] = {'type':[],'input':[],'output':[],'params':{}}
                order.append(name)
            if node.type in op_layer_map:
                d[name]['type'].append(op_layer_map[node.type])
            for input_tensor in node.inputs:
                input_layer_name = get_layer_name(input_tensor.op.name)
                if input_layer_name != name:
                    d[name]['input'].append(input_layer_name)
                    if name not in d[input_layer_name]['output']:
                        d[input_layer_name]['output'].append(name)

        # seperating relu layers
        temp_d = {}
        for layer_name in d:
            if 'ReLU' in d[layer_name]['type']:
                relu_layer_name = layer_name + '_relu'
                temp_d[relu_layer_name] = {'type':['ReLU'],'input':[layer_name],'output':d[layer_name]['output'],'params':{}}
                for output_layer_name in d[layer_name]['output']:
                    for n,i in enumerate(d[output_layer_name]['input']):
                        if i == layer_name:
                            d[output_layer_name]['input'][n] = relu_layer_name
                d[layer_name]['output'] = [relu_layer_name]
        for key in temp_d:
            d[key] = temp_d[key]

        # setting params
        for node in graph.get_operations():
            name = get_layer_name(node.name)
            layer = d[name]

            if layer['type'][0] == 'Input':
                # NCHW to NWHC data format
                layer['params']['dim'] = str(map(int,[node.get_attr('shape').dim[i].size for i in [0,3,1,2]]))[1:-1]

            elif layer['type'][0] == 'Convolution':
                if str(node.name) == name + '/weights':
                    # since conv takes weights as input, this node will be processed first
                    # acquired parameters are then required in get_padding function
                    layer['params']['kernel_h'] = int(node.get_attr('shape').dim[0].size)
                    layer['params']['kernel_w'] = int(node.get_attr('shape').dim[1].size)
                    layer['params']['num_output'] = int(node.get_attr('shape').dim[3].size)
                if str(node.type) == 'Conv2D':
                    layer['params']['stride_h'] = int(node.get_attr('strides')[1])
                    layer['params']['stride_w'] = int(node.get_attr('strides')[2])
                    try:
                        layer['params']['pad_h'],layer['params']['pad_w'] = get_padding(node,layer)
                    except TypeError:
                        return JsonResponse({'result': 'error', 'error': 'Missing shape info in GraphDef'})


            elif layer['type'][0] == 'Pooling':
                if str(node.type) == 'MaxPool':
                    layer['params']['pool'] = 0
                    layer['params']['kernel_h'] = int(node.get_attr('ksize')[1])
                    layer['params']['kernel_w'] = int(node.get_attr('ksize')[2])
                    layer['params']['stride_h'] = int(node.get_attr('strides')[1])
                    layer['params']['stride_w'] = int(node.get_attr('strides')[2])
                    try:
                        layer['params']['pad_h'],layer['params']['pad_w'] = get_padding(node,layer)
                    except TypeError:
                        return JsonResponse({'result': 'error', 'error': 'Missing shape info in GraphDef'})

                if str(node.type) == 'AvgPool':
                    layer['params']['pool'] = 1
                    layer['params']['kernel_h'] = int(node.get_attr('ksize')[1])
                    layer['params']['kernel_w'] = int(node.get_attr('ksize')[2])
                    layer['params']['stride_h'] = int(node.get_attr('strides')[1])
                    layer['params']['stride_w'] = int(node.get_attr('strides')[2])
                    try:
                        layer['params']['pad_h'],layer['params']['pad_w'] = get_padding(node,layer)
                    except TypeError:
                        return JsonResponse({'result': 'error', 'error': 'Missing shape info in GraphDef'})


            elif layer['type'][0] == 'InnerProduct':
                if str(node.name) == name + '/weights':
                    layer['params']['num_output'] = int(node.get_attr('shape').dim[1].size)

            elif layer['type'][0] == 'ReLU':
                pass

            elif layer['type'][0] == 'Concat':
                pass

            elif layer['type'][0] == 'LRN':
                pass

            elif layer['type'][0] == 'Softmax':
                pass

        net = {}
        for key in d:
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
