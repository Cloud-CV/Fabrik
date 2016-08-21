import tensorflow as tf
from google.protobuf import text_format
from tensorflow.core.framework import graph_pb2
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import yaml

op_layer_map = { 'Placeholder':'Input','Conv2D':'Convolution','MaxPool':'Pooling','MatMul':'InnerProduct','Relu':'ReLU','Softmax':'Softmax','LRN':'LRN','Concat':'Concat','AvgPool':'Pooling'}

def get_layer_name(node_name):
    i = node_name.find('/')
    if i == -1:
        name = str(node_name)
    else:
        name = str(node_name[:i])
    return name

@csrf_exempt
def importGraphDef(request):
    if request.method == 'POST':
        f = request.FILES['file']

        graph_def = graph_pb2.GraphDef()
        d = {}
        order = []

        text_format.Merge(f.read(), graph_def)

        for node in graph_def.node:
            name = get_layer_name(node.name)
            if name not in d:
                d[name] = {'type':[],'input':[],'output':[],'params':{}}
                order.append(name)
            if node.op in op_layer_map:
                d[name]['type'].append(op_layer_map[node.op])
            for input_node_name in node.input:
                input_layer_name = get_layer_name(input_node_name)
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
                d[layer_name]['type'].remove('ReLU')
        for key in temp_d:
            d[key] = temp_d[key]

        # setting params
        for node in graph_def.node:
            name = get_layer_name(node.name)
            layer = d[name]

            if layer['type'][0] == 'Input':
                len_dim = len(node.attr['shape'].shape.dim);
                layer['params']['dim'] = str(map(int,[node.attr['shape'].shape.dim[i].size for i in range(len_dim)]))[1:-1]

            elif layer['type'][0] == 'Convolution':
                if str(node.op) == 'Conv2D':
                    layer['params']['stride_h'] = int(node.attr['strides'].list.i[1])
                    layer['params']['stride_w'] = int(node.attr['strides'].list.i[2])
                    layer['params']['pad'] = '' # SAME / VALID ?
                if str(node.name) == name + '/weights':
                    layer['params']['kernel_h'] = int(node.attr['shape'].shape.dim[0].size)
                    layer['params']['kernel_w'] = int(node.attr['shape'].shape.dim[1].size)
                    layer['params']['num_output'] = int(node.attr['shape'].shape.dim[3].size)

            elif layer['type'][0] == 'Pooling':
                if str(node.op) == 'MaxPool':
                    layer['params']['pool'] = 0
                    layer['params']['kernel_h'] = int(node.attr['ksize'].list.i[1])
                    layer['params']['kernel_w'] = int(node.attr['ksize'].list.i[2])
                    layer['params']['stride_h'] = int(node.attr['strides'].list.i[1])
                    layer['params']['stride_w'] = int(node.attr['strides'].list.i[2])
                    layer['params']['pad'] = '' # SAME / VALID ?
                if str(node.op) == 'AvgPool':
                    layer['params']['pool'] = 1
                    layer['params']['kernel_h'] = int(node.attr['ksize'].list.i[1])
                    layer['params']['kernel_w'] = int(node.attr['ksize'].list.i[2])
                    layer['params']['stride_h'] = int(node.attr['strides'].list.i[1])
                    layer['params']['stride_w'] = int(node.attr['strides'].list.i[2])
                    layer['params']['pad'] = '' # SAME / VALID ?

            elif layer['type'][0] == 'InnerProduct':
                if str(node.name) == name + '/weights':
                    layer['params']['num_output'] = int(node.attr['shape'].shape.dim[1].size)

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

