# ********** Data Layers **********
def Input(layer):
    params = {}
    shape = layer.batch_input_shape
    if (len(shape) == 2):
        params['dim'] = str([1, shape[1]])[1:-1]
    else:
        params['dim'] = str([1, shape[3], shape[1], shape[2]])[1:-1]
    return jsonLayer('Input', params, layer)


# ********** Vision Layers **********
def Convolution(layer):
    params = {}
    params['kernel_h'], params['kernel_w'] = layer.kernel_size
    params['stride_h'], params['stride_w'] = layer.strides
    params['dilation_h'], params['dilation_w'] = layer.dilation_rate
    params['pad_h'], params['pad_w'] = get_padding(params['kernel_w'], params['kernel_h'],
                                                   params['stride_w'], params['stride_h'],
                                                   layer.input_shape, layer.output_shape,
                                                   layer.padding.lower())
    params['weight_filler'] = layer.kernel_initializer.__class__.__name__
    params['bias_filler'] = layer.bias_initializer.__class__.__name__
    params['num_output'] = layer.filters
    if (layer.kernel_regularizer):
        params['kernel_regularizer'] = layer.kernel_regularizer.__class__.__name__
    if (layer.bias_regularizer):
        params['bias_regularizer'] = layer.bias_regularizer.__class__.__name__
    if (layer.activity_regularizer):
        params['activity_regularizer'] = layer.activity_regularizer.__class__.__name__
    if (layer.kernel_constraint):
        params['kernel_constraint'] = layer.kernel_constraint.__class__.__name__
    if (layer.bias_constraint):
        params['bias_constraint'] = layer.bias_constraint.__class__.__name__
    params['use_bias'] = layer.use_bias
    return jsonLayer('Convolution', params, layer)


def Deconvolution(layer):
    params = {}
    params['kernel_h'], params['kernel_w'] = layer.kernel_size
    params['stride_h'], params['stride_w'] = layer.strides
    params['dilation_h'], params['dilation_w'] = layer.dilation_rate
    params['pad_h'], params['pad_w'] = get_padding(params['kernel_w'], params['kernel_h'],
                                                   params['stride_w'], params['stride_h'],
                                                   layer.input_shape, layer.output_shape,
                                                   layer.padding.lower())
    params['weight_filler'] = layer.kernel_initializer.__class__.__name__
    params['bias_filler'] = layer.bias_initializer.__class__.__name__
    params['num_output'] = layer.filters
    if (layer.kernel_regularizer):
        params['kernel_regularizer'] = layer.kernel_regularizer.__class__.__name__
    if (layer.bias_regularizer):
        params['bias_regularizer'] = layer.bias_regularizer.__class__.__name__
    if (layer.activity_regularizer):
        params['activity_regularizer'] = layer.activity_regularizer.__class__.__name__
    if (layer.kernel_constraint):
        params['kernel_constraint'] = layer.kernel_constraint.__class__.__name__
    if (layer.bias_constraint):
        params['bias_constraint'] = layer.bias_constraint.__class__.__name__
    params['use_bias'] = layer.use_bias
    return jsonLayer('Deconvolution', params, layer)


def Pooling(layer):
    params = {}
    poolMap = {
        'MaxPooling2D': 0,
        'GlobalMaxPooling2D': 0,
        'AveragePooling2D': 1,
        'GlobalAveragePooling2D': 1
    }
    if (layer.__class__.__name__ in ['GlobalAveragePooling2D', 'GlobalMaxPooling2D']):
        input_shape = layer.input_shape
        params['kernel_h'] = params['stride_h'] = input_shape[2]
        params['kernel_w'] = params['stride_w'] = input_shape[1]
        padding = 'valid'
    else:
        params['kernel_w'], params['kernel_h'] = layer.pool_size
        params['stride_w'], params['stride_h'] = layer.strides
        padding = layer.padding.lower()
    params['pad_h'], params['pad_w'] = get_padding(params['kernel_w'], params['kernel_h'],
                                                   params['stride_w'], params['stride_h'],
                                                   layer.input_shape, layer.output_shape,
                                                   padding)
    params['pool'] = poolMap[layer.__class__.__name__]
    return jsonLayer('Pooling', params, layer)


# ********** Common Layers **********
def Dense(layer):
    params = {}
    params['weight_filler'] = layer.kernel_initializer.__class__.__name__
    params['bias_filler'] = layer.bias_initializer.__class__.__name__
    params['num_output'] = layer.units
    if (layer.kernel_regularizer):
        params['kernel_regularizer'] = layer.kernel_regularizer.__class__.__name__
    if (layer.bias_regularizer):
        params['bias_regularizer'] = layer.bias_regularizer.__class__.__name__
    if (layer.activity_regularizer):
        params['activity_regularizer'] = layer.activity_regularizer.__class__.__name__
    if (layer.kernel_constraint):
        params['kernel_constraint'] = layer.kernel_constraint.__class__.__name__
    if (layer.bias_constraint):
        params['bias_constraint'] = layer.bias_constraint.__class__.__name__
    params['use_bias'] = layer.use_bias
    return jsonLayer('InnerProduct', params, layer)


def Dropout(layer):
    return jsonLayer('Dropout', {}, layer)


def Embed(layer):
    params = {}
    params['input_dim'] = layer.input_dim
    params['num_output'] = layer.output_dim
    params['weight_filler'] = layer.embeddings_initializer.__class__.__name__
    if (layer.embeddings_regularizer):
        params['embeddings_regularizer'] = layer.embeddings_regularizer.__class__.__name__
    if (layer.embeddings_constraint):
        params['embeddings_constraint'] = layer.embeddings_constraint.__class__.__name__
    if (layer.input_length):
        params['input_length'] = layer.input_length
    params['mask_zero'] = layer.mask_zero
    return jsonLayer('Embed', params, layer)


# ********** Recurrent Layers **********
def Recurrent(layer):
    recurrentMap = {
        'SimpleRNN': 'RNN',
        'LSTM': 'LSTM'
    }
    params = {}
    params['num_output'] = layer.units
    params['weight_filler'] = layer.kernel_initializer.__class__.__name__
    params['recurrent_initializer'] = layer.recurrent_initializer.__class__.__name__
    params['bias_filler'] = layer.bias_initializer.__class__.__name__
    if (layer.kernel_regularizer):
        params['kernel_regularizer'] = layer.kernel_regularizer.__class__.__name__
    if (layer.recurrent_regularizer):
        params['recurrent_regularizer'] = layer.recurrent_regularizer.__class__.__name__
    if (layer.bias_regularizer):
        params['bias_regularizer'] = layer.bias_regularizer.__class__.__name__
    if (layer.activity_regularizer):
        params['activity_regularizer'] = layer.activity_regularizer.__class__.__name__
    if (layer.kernel_constraint):
        params['kernel_constraint'] = layer.kernel_constraint.__class__.__name__
    if (layer.recurrent_constraint):
        params['recurrent_constraint'] = layer.recurrent_constraint.__class__.__name__
    if (layer.bias_constraint):
        params['bias_constraint'] = layer.bias_constraint.__class__.__name__
    params['use_bias'] = layer.use_bias
    params['dropout'] = layer.dropout
    params['recurrent_dropout'] = layer.recurrent_dropout
    return jsonLayer(recurrentMap[layer.__class__.__name__], params, layer)


# ********** Normalisation Layers **********
def BatchNorm(layer):
    params = {}
    params['eps'] = layer.epsilon
    params['moving_average_fraction'] = layer.momentum
    params['moving_mean_initializer'] = layer.moving_mean_initializer.__class__.__name__
    params['moving_variance_initializer'] = layer.moving_variance_initializer.__class__.__name__
    return jsonLayer('BatchNorm', params, layer)


# ********** Activation/Neuron Layers **********
def Activation(layer):
    activationMap = {
        'softmax': 'Softmax',
        'relu': 'ReLU',
        'tanh': 'TanH',
        'sigmoid': 'Sigmoid'
    }
    if (layer.__class__.__name__ == 'Activation'):
        return jsonLayer(activationMap[layer.activation.func_name], {}, layer)
    else:
        tempLayer = {}
        tempLayer['inbound_nodes'] = [[[layer.name + layer.__class__.__name__]]]
        return jsonLayer(activationMap[layer.activation.func_name], {}, tempLayer)


def LeakyReLU(layer):
    params = {'negative_slope': layer.alpha.tolist()}
    return jsonLayer('ReLU', params, layer)


def PReLU(layer):
    return jsonLayer('PReLU', {}, layer)


def ELU(layer):
    params = {'alpha': layer.alpha}
    return jsonLayer('ELU', params, layer)


def Scale(layer):
    tempLayer = {}
    params = {}
    params['axis'] = layer.axis
    params['bias_term'] = layer.center
    params['scale'] = layer.scale
    params['filler'] = layer.gamma_initializer.__class__.__name__
    params['bias_filler'] = layer.beta_initializer.__class__.__name__
    params = {'bias_term': layer.center}
    if (layer.beta_regularizer):
        params['beta_regularizer'] = layer.beta_regularizer.__class__.__name__
    if (layer.gamma_regularizer):
        params['gamma_regularizer'] = layer.gamma_regularizer.__class__.__name__
    if (layer.beta_constraint):
        params['beta_constraint'] = layer.beta_constraint.__class__.__name__
    if (layer.gamma_constraint):
        params['gamma_constraint'] = layer.gamma_constraint.__class__.__name__
    tempLayer['inbound_nodes'] = [[[layer.name+layer.__class__.__name__]]]
    return jsonLayer('Scale', params, tempLayer)


# ********** Utility Layers **********
def Flatten(layer):
    return jsonLayer('Flatten', {}, layer)


def Reshape(layer):
    params = {}
    shape = layer.target_shape
    params['dim'] = str([1, shape[2], shape[0], shape[1]])[1:-1]
    return jsonLayer('Reshape', params, layer)


def Concat(layer):
    return jsonLayer('Concat', {}, layer)


def Eltwise(layer):
    eltwiseMap = {
        'Add': 1,
        'Multiply': 0,
        'Maximum': 2
    }
    params = {'operation': eltwiseMap[layer.__class__.__name__]}
    return jsonLayer('Eltwise', params, layer)


def Padding(layer):
    pad = layer.padding
    params = {'pad_h': pad[0][0], 'pad_w': pad[1][0]}
    return jsonLayer('Pad', params, layer)


# ********** Helper functions **********

# padding logic following
# https://github.com/Yangqing/caffe2/blob/master/caffe2/proto/caffe2_legacy.proto
def get_padding(k_w, k_h, s_w, s_h, input_shape, output_shape, pad_type):
    if (pad_type == 'valid'):
        return [0, 0]
    else:
        pad_h = ((output_shape[2]-1)*s_h + k_h - input_shape[2])/2
        pad_w = ((output_shape[1]-1)*s_w + k_w - input_shape[1])/2
        return (pad_h, pad_w)


def jsonLayer(type, params, layer):
    input = []
    if isinstance(layer, dict):
        for node in layer['inbound_nodes'][0]:
            input.append(node[0])
    elif (len(layer.inbound_nodes[0].inbound_layers)):
        for node in layer.inbound_nodes[0].inbound_layers:
            input.append(node.name)
    layer = {
                'info': {
                    'type': type,
                    'phase': None
                },
                'connection': {
                    'input': input,
                    'output': []
                },
                'params': params
            }
    return layer
