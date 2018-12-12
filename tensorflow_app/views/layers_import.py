import math
import re


initializer_map = {'random_uniform': 'RandomUniform', 'random_normal': 'RandomNormal',
                   'Const': 'Constant', 'zeros': 'Zeros', 'ones': 'Ones',
                   'eye': 'Identity', 'truncated_normal': 'TruncatedNormal'}

activation_layers = [
    'Sigmoid',
    'Softplus',
    'Softsign',
    'Elu',
    'LeakyRelu',
    'Softmax',
    'Relu',
    'Tanh',
    'SELU'
]


def get_layer_name(node_name):
    i = node_name.find('/')
    if i == -1:
        name = str(node_name)
    elif str(node_name[:i]) in ['Repeat', 'Stack']:
        name = str(node_name.split('/')[1])
    else:
        name = str(node_name[:i])
    return name


def get_layer_type(node_name):
    return node_name.split('_')[0]


def get_padding(node, kernel_shape, strides):
    if node.type in ["Conv3D", "MaxPool3D", "AvgPool3D"]:
        input_tensor = node.inputs[0]
        output_tensor = node.outputs[0]
        input_shape = [1 if i.value is None else int(i) for i in input_tensor.shape]
        output_shape = [1 if i.value is None else int(i) for i in output_tensor.shape]

        kernel_d = kernel_shape[0]
        kernel_h = kernel_shape[1]
        kernel_w = kernel_shape[2]
        stride_d = strides[1]
        stride_h = strides[2]
        stride_w = strides[3]

        pad_d = ((int(output_shape[1]) - 1) * stride_d +
                 kernel_d - int(input_shape[1])) / float(2)
        pad_h = ((int(output_shape[2]) - 1) * stride_h +
                 kernel_h - int(input_shape[2])) / float(2)
        pad_w = ((int(output_shape[3]) - 1) * stride_w +
                 kernel_w - int(input_shape[3])) / float(2)

        if node.type == "Conv3D":
            pad_d = math.ceil(pad_d)
            pad_h = math.ceil(pad_h)
            pad_w = math.ceil(pad_w)
        elif node.type in ["MaxPool3D", "AvgPool3D"]:
            pad_d = math.floor(pad_d)
            pad_h = math.floor(pad_h)
            pad_w = math.floor(pad_w)

        return int(pad_d), int(pad_h), int(pad_w)

    elif node.type == "Conv2DBackpropInput":
        input_tensor = node.inputs[2]
        output_tensor = node.outputs[0]
        input_shape = [1 if i.value is None else int(i) for i in input_tensor.shape]
        output_shape = [1 if i.value is None else int(i) for i in output_tensor.shape]

        # if deconvolution layer padding calculation logic changes
        if ('padding' in node.node_def.attr):
            kernel_h = kernel_shape[0]
            kernel_w = kernel_shape[1]
            stride_h = strides[1]
            stride_w = strides[2]
            pad_h = ((int(input_shape[1]) - 1) * stride_h +
                     kernel_h - int(output_shape[1])) / float(2)
            pad_w = ((int(input_shape[2]) - 1) * stride_w +
                     kernel_w - int(output_shape[2])) / float(2)

            return int(math.floor(pad_h)), int(math.floor(pad_w))

    else:
        input_tensor = node.inputs[0]
        output_tensor = node.outputs[0]
        input_shape = [1 if i.value is None else int(i) for i in input_tensor.shape]
        output_shape = [1 if i.value is None else int(i) for i in output_tensor.shape]
        kernel_h = kernel_shape[0]
        kernel_w = kernel_shape[1]
        stride_h = strides[1]
        stride_w = strides[2]

        pad_h = ((int(output_shape[1]) - 1) * stride_h +
                 kernel_h - int(input_shape[1])) / float(2)
        pad_w = ((int(output_shape[2]) - 1) * stride_w +
                 kernel_w - int(input_shape[2])) / float(2)

        # check this logic (see caffe-tensorflow/caffe/shapes.py)
        if node.type == "Conv2D":
            pad_h = math.ceil(pad_h)
            pad_w = math.ceil(pad_w)
        elif node.type in ["MaxPool", "AvgPool"]:
            pad_h = math.floor(pad_h)
            pad_w = math.floor(pad_w)

        return int(pad_h), int(pad_w)


def get_initializer_type(layer_ops):
    """Returns a dict mapping variables (weight, bias etc) to initializer types.
    The returned dict maybe empty if no initializers are found.
    """
    weight_name_patterns = [r'.*/weight/*', r'.*/kernel/*']
    bias_name_patterns = [r'.*/bias/*']
    pointwise_weight_name_patterns = [r'.*/pointwise_weights/*']
    depthwise_weight_name_patterns = [r'.*/depthwise_weights/*']

    initializers = {}
    for op in layer_ops:
        # extracting weights initializer
        for weight_name_pattern in weight_name_patterns:
            if re.match(weight_name_pattern, str(op.name)) and op.type in initializer_map.keys():
                initializers['weight'] = initializer_map[op.type]
        # extracting bias initializer
        for bias_name_pattern in bias_name_patterns:
            if re.match(bias_name_pattern, str(op.name)) and op.type in initializer_map.keys():
                initializers['bias'] = initializer_map[op.type]
        # extracting pointwise wei
        for pointwise_weight_name_pattern in pointwise_weight_name_patterns:
            if re.match(pointwise_weight_name_pattern, str(op.name)) and op.type in initializer_map.keys():
                initializers['pointwise_weight'] = initializer_map[op.type]
        for depthwise_weight_name_pattern in depthwise_weight_name_patterns:
            if re.match(depthwise_weight_name_pattern, str(op.name)) and op.type in initializer_map.keys():
                initializers['depthwise_weight'] = initializer_map[op.type]

    return initializers


def get_input_layers(layer_ops):
    '''
    return the name of the layers directly preceeding the layer of layer_ops.
    layer_ops is a list of all ops of the layer we want the inputs of.
    '''
    input_layer_names = []
    name = get_layer_name(layer_ops[0].name)
    for node in layer_ops:
        for input_tensor in node.inputs:
            input_layer_name = get_layer_name(input_tensor.op.name)
            if input_layer_name != name:
                input_layer_names.append(input_layer_name)
    return input_layer_names


def import_activation(layer_ops):
    layer_type = ''
    layer_params = {}

    activation_op = next((x for x in layer_ops if x.type in activation_layers), None)

    if activation_op.type == 'Relu':
        layer_type = 'ReLU'

    elif activation_op.type == 'LeakyRelu':
        if 'alpha' in activation_op.node_def.attr:
            layer_params['negative_slope'] = activation_op.get_attr('alpha')
        layer_type = 'ReLU'

    elif activation_op.type == 'Elu':
        layer_params['alpha'] = 1
        layer_type = 'ELU'

    elif activation_op.type == 'Tanh':
        layer_type = 'TanH'

    else:
        # rest of the activations have the same name in TF and Fabrik
        layer_type = activation_op.type

    return jsonLayer(layer_type, layer_params, get_input_layers(layer_ops), [])


def import_placeholder(layer_ops):
    placeholder_op = layer_ops[0]
    layer_params = {}
    layer_dim = [int(dim.size) for dim in placeholder_op.get_attr('shape').dim]

    # make batch size 1 if it is -1
    if layer_dim[0] == 0:
        layer_dim[0] = 1

    # change tensor format from tensorflow default (NHWC/NDHWC)
    # to (NCHW/NCDHW)
    temp = layer_dim[1]
    layer_dim[1] = layer_dim[-1]
    layer_dim[-1] = temp
    layer_params['dim'] = str(layer_dim)[1:-1]

    return jsonLayer('Input', layer_params, get_input_layers(layer_ops), [])


def import_conv2d(layer_ops):
    conv2d_op = next((x for x in layer_ops if x.type == 'Conv2D'), None)
    layer_params = {}
    layer_params['layer_type'] = '2D'

    strides = [int(i) for i in conv2d_op.get_attr('strides')]
    kernel_shape = [int(i) for i in conv2d_op.inputs[1].shape]
    layer_params['stride_h'] = strides[1]
    layer_params['stride_w'] = strides[2]
    layer_params['kernel_h'] = kernel_shape[0]
    layer_params['kernel_w'] = kernel_shape[1]
    layer_params['num_output'] = kernel_shape[3]
    layer_params['pad_h'], layer_params['pad_w'] = get_padding(conv2d_op, kernel_shape, strides)

    initializers = get_initializer_type(layer_ops)
    try:
        layer_params['weight_filler'] = initializers['kernel']
        layer_params['bias_filler'] = initializers['bias']
    except KeyError:
        # no initializers found, continue
        pass

    return jsonLayer('Convolution', layer_params, get_input_layers(layer_ops), [])


def import_conv3d(layer_ops):
    conv3d_op = next((x for x in layer_ops if x.type == 'Conv3D'), None)
    layer_params = {}
    layer_params['layer_type'] = '3D'

    kernel_shape = [int(i) for i in conv3d_op.inputs[1].shape]
    layer_params['kernel_d'] = kernel_shape[0]
    layer_params['kernel_h'] = kernel_shape[1]
    layer_params['kernel_w'] = kernel_shape[2]
    layer_params['num_output'] = kernel_shape[4]

    strides = [int(i) for i in conv3d_op.get_attr('strides')]
    layer_params['stride_d'] = strides[1]
    layer_params['stride_h'] = strides[2]
    layer_params['stride_w'] = strides[3]

    pad_d, pad_h, pad_w = get_padding(conv3d_op, kernel_shape, strides)
    layer_params['pad_d'] = pad_d
    layer_params['pad_h'] = pad_h
    layer_params['pad_w'] = pad_w

    initializers = get_initializer_type(layer_ops)
    try:
        layer_params['weight_filler'] = initializers['kernel']
        layer_params['bias_filler'] = initializers['bias']
    except KeyError:
        # no initializers found, continue
        pass

    return jsonLayer('Convolution', layer_params, get_input_layers(layer_ops), [])


def import_deconvolution(layer_ops):
    deconv_op = next((x for x in layer_ops if x.type == 'Conv2DBackpropInput'), None)
    layer_params = {}
    layer_params['layer_type'] = '2D'

    kernel_shape = [int(i) for i in deconv_op.inputs[1].shape]
    strides = [int(i) for i in deconv_op.get_attr('strides')]
    layer_params['padding'] = deconv_op.get_attr('padding')
    layer_params['kernel_h'] = kernel_shape[0]
    layer_params['kernel_w'] = kernel_shape[1]
    layer_params['num_output'] = kernel_shape[3]
    layer_params['pad_h'], layer_params['pad_w'] = get_padding(deconv_op, kernel_shape, strides)

    initializers = get_initializer_type(layer_ops)
    try:
        layer_params['weight_filler'] = initializers['kernel']
        layer_params['bias_filler'] = initializers['bias']
    except KeyError:
        # no initializers found, continue
        pass

    return jsonLayer('Deconvolution', layer_params, get_input_layers(layer_ops), [])


def import_depthwise_convolution(layer_ops):
    depthwise_conv_op = next((x for x in layer_ops if x.type == 'DepthwiseConv2dNative'), None)
    layer_params = {}
    if '3D' in depthwise_conv_op.type:
        raise ValueError('3D depthwise convolution cannot be imported.')

    kernel_shape = [int(i) for i in depthwise_conv_op.inputs[1].shape]
    layer_params['kernel_h'] = kernel_shape[0]
    layer_params['kernel_w'] = kernel_shape[1]
    layer_params['num_output'] = kernel_shape[2]
    layer_params['depth_multiplier'] = kernel_shape[3]

    if 'padding' in depthwise_conv_op.node_def.attr:
        layer_params['padding'] = str(depthwise_conv_op.get_attr('padding'))
    strides = [int(i) for i in depthwise_conv_op.get_attr('strides')]
    layer_params['stride_h'] = strides[1]
    layer_params['stride_w'] = strides[2]
    layer_params['pad_h'], layer_params['pad_w'] = get_padding(depthwise_conv_op, kernel_shape, strides)

    initializers = get_initializer_type(layer_ops)
    try:
        layer_params['pointwise_weight'] = initializers['pointwise_initializer']
        layer_params['depthwise_weight'] = initializers['depthwise_initializer']
    except KeyError:
        # no initializers found, continue
        pass

    return jsonLayer('DepthwiseConv', layer_params, get_input_layers(layer_ops), [])


def import_pooling2d(layer_ops):
    pooling2d_op = next((x for x in layer_ops if x.type in ['MaxPool', 'AvgPool']))
    layer_params = {}
    layer_params['layer_type'] = '2D'

    # checking type of pooling layer
    if pooling2d_op.type == 'MaxPool':
        layer_params['pool'] = 'MAX'
    elif pooling2d_op.type == 'AvgPool':
        layer_params['pool'] = 'AVE'

    kernel_shape = [int(i) for i in pooling2d_op.get_attr('ksize')]
    strides = [int(i) for i in pooling2d_op.get_attr('strides')]
    layer_params['kernel_h'] = kernel_shape[1]
    layer_params['kernel_w'] = kernel_shape[2]
    layer_params['stride_h'] = strides[1]
    layer_params['stride_w'] = strides[2]
    layer_params['padding'] = str(pooling2d_op.get_attr('padding'))
    layer_params['pad_h'], layer_params['pad_w'] = get_padding(pooling2d_op, kernel_shape, strides)

    return jsonLayer('Pooling', layer_params, get_input_layers(layer_ops), [])


def import_pooling3d(layer_ops):
    pooling3d_op = next((x for x in layer_ops if x.type in ['MaxPool3D', 'AvgPool3D']))
    layer_params = {}
    layer_params['layer_type'] = '3D'
    layer_params['padding'] = str(pooling3d_op.get_attr('padding'))

    # checking type of pooling layer
    if pooling3d_op.type == 'MaxPool':
        layer_params['pool'] = 'MAX'
    elif pooling3d_op.type == 'AvgPool':
        layer_params['pool'] = 'AVE'

    kernel_shape = [int(i) for i in pooling3d_op.get_attr('ksize')]
    strides = [int(i) for i in pooling3d_op.get_attr('strides')]
    layer_params['kernel_d'] = kernel_shape[1]
    layer_params['kernel_h'] = kernel_shape[2]
    layer_params['kernel_w'] = kernel_shape[3]
    layer_params['stride_d'] = strides[1]
    layer_params['stride_h'] = strides[2]
    layer_params['stride_w'] = strides[3]

    pad_d, pad_h, pad_w = get_padding(pooling3d_op, kernel_shape, strides)
    layer_params['pad_d'] = pad_d
    layer_params['pad_h'] = pad_h
    layer_params['pad_w'] = pad_w

    return jsonLayer('Pooling', layer_params, get_input_layers(layer_ops), [])


def import_inner_product(layer_ops):
    inner_product_op = next((x for x in layer_ops if x.type in ['Prod', 'MatMul']))
    layer_params = {}
    if inner_product_op.type == 'MatMul':
        layer_params['num_output'] = int(inner_product_op.inputs[1].shape[1])

    return jsonLayer('InnerProduct', layer_params, get_input_layers(layer_ops), [])


def import_batchnorm(layer_ops):
    layer_params = {}
    name = get_layer_name(layer_ops[0].name)

    for node in layer_ops:
        if re.match('.*\/batchnorm[_]?[0-9]?\/add.*', str(node.name)):
            try:
                layer_params['eps'] = node.get_attr('value').float_val[0]
            except:
                pass
        if (node.type == 'FusedBatchNorm'):
            layer_params['eps'] = float(node.get_attr('epsilon'))
        # searching for moving_mean/Initializer ops to extract moving
        # mean initializer of batchnorm layer
        if name + '/moving_mean/Initializer' in str(node.name):
            layer_params['moving_mean_initializer'] = \
                initializer_map[str(node.name).split('/')[3]]
        # searching for AssignMovingAvg/decay ops to extract moving
        # average fraction of batchnorm layer also considering repeat & stack layer
        # as prefixes
        if str(node.name) in [name + '/AssignMovingAvg/decay',
                              'Repeat/' + name + '/AssignMovingAvg/decay',
                              'Stack/' + name + '/AssignMovingAvg/decay']:
            layer_params['moving_average_fraction'] = node.get_attr(
                'value').float_val[0]

    return jsonLayer('BatchNorm', layer_params, get_input_layers(layer_ops), [])


def import_eltwise(layer_ops):
    eltwise_op = next((x for x in layer_ops if x.type in ['add', 'mul', 'dot']))
    layer_params = {}
    if eltwise_op.type == 'add':
        layer_params['layer_type'] = 'Sum'
    if eltwise_op.type == 'mul':
        layer_params['layer_type'] = 'Product'
    if eltwise_op.type == 'dot':
        layer_params['layer_type'] = 'Dot'

    return jsonLayer('Eltwise', layer_params, get_input_layers(layer_ops), [])


def import_dropout(layer_ops):
    layer_params = {}
    for node in layer_ops:
        if ('rate' in node.node_def.attr):
            layer_params['rate'] = node.get_attr('rate')
        if ('seed' in node.node_def.attr):
            layer_params['seed'] = node.get_attr('seed')
        if ('training' in node.node_def.attr):
            layer_params['trainable'] = node.get_attr('training')

    return jsonLayer('Dropout', layer_params, get_input_layers(layer_ops), [])


def import_flatten(layer_ops):
    return jsonLayer('Flatten', [], get_input_layers(layer_ops), [])


def import_concat(layer_ops):
    layer_params = {}
    for node in layer_ops:
        if 'axis' in node.node_def.attr:
            layer_params['axis'] = node.get_attr('axis')

    return jsonLayer('Concat', layer_params, get_input_layers(layer_ops), [])


def import_lrn(layer_ops):
    layer_params = {}
    for node in layer_ops:
        if ('alpha' in node.node_def.attr):
            layer_params['alpha'] = node.get_attr('alpha')
        if ('beta' in node.node_def.attr):
            layer_params['beta'] = node.get_attr('beta')
        if ('local_size' in node.node_def.attr):
            layer_params['local_size'] = node.get_attr('depth_radius')
        if ('bias' in node.node_def.attr):
            layer_params['k'] = node.get_attr('bias')

    return jsonLayer('LRN', layer_params, get_input_layers(layer_ops), [])


def jsonLayer(layer_type, layer_params={}, inputs=[], outputs=[]):
    layer = {
        'info': {
            'type': layer_type,
            'phase': None
        },
        'connection': {
            'input': inputs,
            'output': outputs
        },
        'params': layer_params
    }
    return layer
