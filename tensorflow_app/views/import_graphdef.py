import tensorflow as tf
from google.protobuf import text_format
from tensorflow.core.framework import graph_pb2
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import urllib2
from urlparse import urlparse

from layers_import import import_placeholder, import_conv2d, import_conv3d, import_deconvolution, \
                        import_depthwise_convolution, import_pooling2d, import_pooling3d, \
                        import_inner_product, import_batchnorm, import_eltwise, import_activation, \
                        import_dropout, import_flatten, import_concat, import_lrn

from layers_import import get_layer_name, get_layer_type, jsonLayer, activation_layers

layer_map = {
    'Placeholder': import_placeholder,
    'Conv2D': import_conv2d,
    'Conv3D': import_conv3d,
    'MaxPool': import_pooling2d,
    'MaxPool3D': import_pooling3d,
    'AvgPool3D': import_pooling3d,
    'DepthwiseConv2dNative': import_depthwise_convolution,
    'FusedBatchNorm': import_batchnorm,
    'Conv2DBackpropInput': import_deconvolution,
    'LRN': import_lrn,
    'MatMul': import_inner_product,
    'Prod': import_inner_product,
    'Concat': import_concat,
    'AvgPool': import_pooling2d,
    'Reshape': import_flatten
}

name_map = {
    'flatten': import_flatten,
    'dropout': import_dropout,
    'lrn': import_lrn,
    'concatenate': import_concat,
    'batch': import_batchnorm,
    'BatchNorm': import_batchnorm,
    'add': import_eltwise,
    'mul': import_eltwise
}


def get_all_ops_in_layer(layer_name, all_ops):
    ops_from_same_layer = []
    for op in all_ops:
        if get_layer_name(op.name) == layer_name:
            ops_from_same_layer.append(op)
    return ops_from_same_layer


@csrf_exempt
def import_graph_def(request):
    if request.method == 'POST':
        if ('file' in request.FILES) and \
           (request.FILES['file'].content_type == 'application/octet-stream' or
                request.FILES['file'].content_type == 'text/plain'):
            try:
                f = request.FILES['file']
                config = f.read()
                f.close()
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

        try:
            text_format.Merge(config, graph_def)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid GraphDef'})

        tf.import_graph_def(graph_def, name='')
        graph = tf.get_default_graph()
        session = tf.Session(graph=graph)
        all_ops = graph.get_operations()

        net = {}
        processed_layers = []
        layers_with_inplace_relu = {}

        for node in all_ops:

            layer_name = get_layer_name(node.name)
            layer_type = get_layer_type(node.name)

            if layer_name in processed_layers:
                continue

            if node.type == 'NoOp':
                init_op = session.graph.get_operation_by_name(node.name)
                session.run(init_op)
                continue

            all_ops_in_layer = get_all_ops_in_layer(layer_name, all_ops)
            for op in all_ops_in_layer:
                if op.type == 'FusedBatchNorm':
                    net[layer_name] = import_batchnorm(all_ops_in_layer)
                    processed_layers.append(layer_name)

            if node.type in layer_map:
                for i, op in enumerate(all_ops_in_layer):
                    # if the layer has an inplace relu operation, separate the relu op
                    # this prevents net[layer_name] from being overwritten by an inplace
                    # relu layer when the layer might actually contain another important
                    # layer like a dense layer for example
                    if op.type == 'Relu':
                        del(all_ops_in_layer[i])
                        relu_layer = jsonLayer('ReLU', {}, [layer_name])
                        relu_layer_name = layer_name + '_relu'
                        net[relu_layer_name] = relu_layer
                        layers_with_inplace_relu[layer_name] = relu_layer_name
                json_layer = layer_map[node.type](all_ops_in_layer)
                net[layer_name] = json_layer
                processed_layers.append(layer_name)

            elif node.type in activation_layers:
                json_layer = import_activation(all_ops_in_layer)
                net[layer_name] = json_layer
                processed_layers.append(layer_name)

            elif layer_type in name_map:
                json_layer = name_map[layer_type](all_ops_in_layer)
                net[layer_name] = json_layer
                processed_layers.append(layer_name)

        # connect layers with the previous layer's inplace relu ops, if any
        for layer_name in net:
            for i, input_layer in enumerate(net[layer_name]['connection']['input']):
                if (input_layer in layers_with_inplace_relu.keys()) and \
                        layers_with_inplace_relu[input_layer] != layer_name:
                    net[layer_name]['connection']['input'][i] = layers_with_inplace_relu[input_layer]

        # fill in outputs of every layer in net using inputs of consumer layers
        outputs = {}
        for layer_name in net.keys():
            for input_layer_name in net[layer_name]['connection']['input']:
                if input_layer_name not in outputs:
                    outputs[input_layer_name] = []
                if layer_name not in outputs[input_layer_name]:
                    outputs[input_layer_name].append(layer_name)
        for layer in outputs:
            net[layer]['connection']['output'] = outputs[layer]

        # add a scale layer next to batch normalization layers
        scale_layers = {}
        for layer_name in net:
            if net[layer_name]['info']['type'] == 'BatchNorm':
                batch_norm_outputs = net[layer_name]['connection']['output'][:]
                scale_layer_name = layer_name + '_scale'
                scale_layer = jsonLayer('Scale', {}, [layer_name], batch_norm_outputs)
                net[layer_name]['connection']['output'] = [scale_layer_name]
                scale_layers[scale_layer_name] = scale_layer
        for scale_layer_name in scale_layers:
            net[scale_layer_name] = scale_layers[scale_layer_name]

        session.close()

        return JsonResponse({'result': 'success', 'net': net, 'net_name': ''})
