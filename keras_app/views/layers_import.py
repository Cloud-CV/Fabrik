import numpy as np


# ********** Data Layers **********
def Input(layer):
    params = {}
    shape = layer.batch_input_shape
    if (len(shape) == 2):
        params['dim'] = str([1, shape[1]])[1:-1]
    else:
        params['dim'] = str([1, shape[-1]] + list(shape[1:-1]))[1:-1]
    return jsonLayer('Input', params, layer)


# ********** Core Layers **********
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


def Activation(layer):
    activationMap = {
        'softmax': 'Softmax',
        'relu': 'ReLU',
        'tanh': 'TanH',
        'sigmoid': 'Sigmoid',
        'selu': 'SELU',
        'softplus': 'Softplus',
        'softsign': 'Softsign',
        'hard_sigmoid': 'HardSigmoid',
        'linear': 'Linear'
    }
    if (layer.__class__.__name__ == 'Activation'):
        return jsonLayer(activationMap[layer.activation.func_name], {}, layer)
    else:
        tempLayer = {}
        tempLayer['inbound_nodes'] = [
            [[layer.name + layer.__class__.__name__]]]
        return jsonLayer(activationMap[layer.activation.func_name], {}, tempLayer)


def Dropout(layer):
    params = {}
    if (layer.rate is not None):
        params['rate'] = layer.rate
    if (layer.seed is not None):
        params['seed'] = layer.seed
    if (layer.trainable is not None):
        params['trainable'] = layer.trainable
    return jsonLayer('Dropout', params, layer)


def Flatten(layer):
    return jsonLayer('Flatten', {}, layer)


def Reshape(layer):
    params = {}
    shape = layer.target_shape
    params['dim'] = str([1] + list(shape))[1:-1]
    return jsonLayer('Reshape', params, layer)


def Permute(layer):
    params = {}
    params['dim'] = str(layer.dims)[1:-1]
    return jsonLayer('Permute', params, layer)


def RepeatVector(layer):
    params = {}
    params['n'] = layer.n
    return jsonLayer('RepeatVector', params, layer)


def ActivityRegularization(layer):
    params = {}
    params['l1'] = layer.l1
    params['l2'] = layer.l2
    return jsonLayer('Regularization', params, layer)


def Masking(layer):
    params = {}
    params['mask_value'] = layer.mask_value
    return jsonLayer('Masking', params, layer)


# ********** Convolutional Layers **********
def Convolution(layer):
    params = {}
    if (layer.__class__.__name__ == 'Conv1D'):
        params['layer_type'] = '1D'
        params['kernel_w'] = layer.kernel_size[0]
        params['stride_w'] = layer.strides[0]
        params['dilation_w'] = layer.dilation_rate[0]
        params['pad_w'] = get_padding([params['kernel_w'], -1, -1,
                                       params['stride_w'], -1, -1],
                                      layer.input_shape, layer.output_shape,
                                      layer.padding.lower(), '1D')
    elif (layer.__class__.__name__ == 'Conv2D'):
        params['layer_type'] = '2D'
        params['kernel_h'], params['kernel_w'] = layer.kernel_size
        params['stride_h'], params['stride_w'] = layer.strides
        params['dilation_h'], params['dilation_w'] = layer.dilation_rate
        params['pad_h'], params['pad_w'] = get_padding([params['kernel_w'], params['kernel_h'], -1,
                                                        params['stride_w'], params['stride_h'], -1],
                                                       layer.input_shape, layer.output_shape,
                                                       layer.padding.lower(), '2D')
    else:
        params['layer_type'] = '3D'
        params['kernel_h'], params['kernel_w'], params['kernel_d'] = layer.kernel_size
        params['stride_h'], params['stride_w'], params['stride_d'] = layer.strides
        params['dilation_h'], params['dilation_w'], params['dilation_d'] = layer.dilation_rate
        params['pad_h'], params['pad_w'], params['pad_d'] = get_padding([params['kernel_w'],
                                                                         params['kernel_h'],
                                                                         params['kernel_d'],
                                                                         params['stride_w'],
                                                                         params['stride_h'],
                                                                         params['stride_d']],
                                                                        layer.input_shape,
                                                                        layer.output_shape,
                                                                        layer.padding.lower(), '3D')
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


# Separable Convolution is currently not supported with Theano backend

def DepthwiseConv(layer):
    params = {}
    params['num_output'] = layer.filters
    params['kernel_h'], params['kernel_w'] = layer.kernel_size
    params['stride_h'], params['stride_w'] = layer.strides
    params['pad_h'], params['pad_w'] = get_padding([params['kernel_w'], params['kernel_h'], -1,
                                                    params['stride_w'], params['stride_h'], -1],
                                                   layer.input_shape, layer.output_shape,
                                                   layer.padding.lower(), '2D')
    params['depth_multiplier'] = layer.depth_multiplier
    params['use_bias'] = layer.use_bias
    params['depthwise_initializer'] = layer.depthwise_initializer.__class__.__name__
    params['pointwise_initializer'] = layer.pointwise_initializer.__class__.__name__
    params['bias_initializer'] = layer.bias_initializer.__class__.__name__
    if (layer.depthwise_regularizer):
        params['depthwise_regularizer'] = layer.depthwise_regularizer.__class__.__name__
    if (layer.pointwise_regularizer):
        params['pointwise_regularizer'] = layer.pointwise_regularizer.__class__.__name__
    if (layer.bias_regularizer):
        params['bias_regularizer'] = layer.bias_regularizer.__class__.__name__
    if (layer.activity_regularizer):
        params['activity_regularizer'] = layer.activity_regularizer.__class__.__name__
    if (layer.depthwise_constraint):
        params['depthwise_constraint'] = layer.depthwise_constraint.__class__.__name__
    if (layer.pointwise_constraint):
        params['pointwise_constraint'] = layer.pointwise_constraint.__class__.__name__
    if (layer.bias_constraint):
        params['bias_constraint'] = layer.bias_constraint.__class__.__name__
    return jsonLayer('DepthwiseConv', params, layer)


def Deconvolution(layer):
    params = {}
    params['kernel_h'], params['kernel_w'] = layer.kernel_size
    params['stride_h'], params['stride_w'] = layer.strides
    params['dilation_h'], params['dilation_w'] = layer.dilation_rate
    params['pad_h'], params['pad_w'] = get_padding([params['kernel_w'], params['kernel_h'], -1,
                                                    params['stride_w'], params['stride_h'], -1],
                                                   layer.input_shape, layer.output_shape,
                                                   layer.padding.lower(), '2D')
    params['padding'] = layer.padding.upper()
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


def Upsample(layer):
    params = {}
    if (layer.__class__.__name__ == 'UpSampling1D'):
        params['size_w'] = layer.size
        params['layer_type'] = '1D'
    elif (layer.__class__.__name__ == 'UpSampling2D'):
        params['size_w'], params['size_h'] = layer.size
        params['layer_type'] = '2D'
    else:
        params['size_w'], params['size_h'], params['size_d'] = layer.size
        params['layer_type'] = '3D'
    return jsonLayer('Upsample', params, layer)


# ********** Pooling Layers **********
def Pooling(layer):
    params = {}
    poolMap = {
        'MaxPooling1D': 'MAX',
        'MaxPooling2D': 'MAX',
        'MaxPooling3D': 'MAX',
        'AveragePooling1D': 'AVE',
        'AveragePooling2D': 'AVE',
        'AveragePooling3D': 'AVE',
        'GlobalMaxPooling1D': 'MAX',
        'GlobalMaxPooling2D': 'MAX',
        'GlobalAveragePooling1D': 'AVE',
        'GlobalAveragePooling2D': 'AVE'
    }
    if (layer.__class__.__name__ in ['GlobalAveragePooling1D', 'GlobalMaxPooling1D']):
        input_shape = layer.input_shape
        params['kernel_w'] = params['stride_w'] = input_shape[1]
        padding = 'valid'
        params['layer_type'] = '1D'
        params['pad_w'] = get_padding([params['kernel_w'], -1, -1,
                                       params['stride_w'], -1, -1],
                                      layer.input_shape, layer.output_shape,
                                      padding, '1D')
    elif (layer.__class__.__name__ in ['GlobalAveragePooling2D', 'GlobalMaxPooling2D']):
        input_shape = layer.input_shape
        params['kernel_h'] = params['stride_h'] = input_shape[2]
        params['kernel_w'] = params['stride_w'] = input_shape[1]
        padding = 'valid'
        params['layer_type'] = '2D'
        params['pad_h'], params['pad_w'] = get_padding([params['kernel_w'], params['kernel_h'], -1,
                                                        params['stride_w'], params['stride_h'], -1],
                                                       layer.input_shape, layer.output_shape,
                                                       padding, '2D')
    else:
        padding = layer.padding.lower()
        if (layer.__class__.__name__ in ['MaxPooling1D', 'AveragePooling1D']):
            params['kernel_w'] = layer.pool_size[0]
            params['stride_w'] = layer.strides[0]
            params['layer_type'] = '1D'
            params['pad_w'] = get_padding([params['kernel_w'], -1, -1,
                                           params['stride_w'], -1, -1],
                                          layer.input_shape, layer.output_shape,
                                          padding, '1D')
        elif (layer.__class__.__name__ in ['MaxPooling2D', 'AveragePooling2D']):
            params['kernel_w'], params['kernel_h'] = layer.pool_size
            params['stride_w'], params['stride_h'] = layer.strides
            params['layer_type'] = '2D'
            params['pad_h'], params['pad_w'] = get_padding([params['kernel_w'], params['kernel_h'], -1,
                                                            params['stride_w'], params['stride_h'], -1],
                                                           layer.input_shape, layer.output_shape,
                                                           padding, '2D')
        else:
            params['kernel_h'], params['kernel_w'], params['kernel_d'] = layer.pool_size
            params['stride_h'], params['stride_w'], params['stride_d'] = layer.strides
            params['layer_type'] = '3D'
            params['pad_h'], params['pad_w'], params['pad_d'] = get_padding([params['kernel_w'],
                                                                             params['kernel_h'],
                                                                             params['kernel_d'],
                                                                             params['stride_w'],
                                                                             params['stride_h'],
                                                                             params['stride_d']],
                                                                            layer.input_shape,
                                                                            layer.output_shape,
                                                                            padding, '3D')
    params['pool'] = poolMap[layer.__class__.__name__]
    return jsonLayer('Pooling', params, layer)


# ********** Locally-connected Layers **********
def LocallyConnected(layer):
    params = {}
    if (layer.__class__.__name__ == 'LocallyConnected1D'):
        params['layer_type'] = '1D'
        params['kernel_w'] = layer.kernel_size[0]
        params['stride_w'] = layer.strides[0]
    else:
        params['layer_type'] = '2D'
        params['kernel_h'], params['kernel_w'] = layer.kernel_size
        params['stride_h'], params['stride_w'] = layer.strides
    params['kernel_initializer'] = layer.kernel_initializer.__class__.__name__
    params['bias_initializer'] = layer.bias_initializer.__class__.__name__
    params['filters'] = layer.filters
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
    return jsonLayer('LocallyConnected', params, layer)


# ********** Recurrent Layers **********
def Recurrent(layer):
    recurrentMap = {
        'SimpleRNN': 'RNN',
        'GRU': 'GRU',
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
    if (layer.__class__.__name__ == 'GRU'):
        params['recurrent_activation'] = layer.recurrent_activation.func_name
    elif (layer.__class__.__name__ == 'LSTM'):
        params['recurrent_activation'] = layer.recurrent_activation.func_name
        params['unit_forget_bias'] = layer.unit_forget_bias
        params['return_sequences'] = layer.return_sequences
    return jsonLayer(recurrentMap[layer.__class__.__name__], params, layer)


# ********** Embedding Layers **********
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


# ********** Merge Layers **********
def Concat(layer):
    params = {}
    params['axis'] = layer.axis
    return jsonLayer('Concat', params, layer)


def Eltwise(layer):
    eltwiseMap = {
        'Add': 'Sum',
        'Multiply': 'Product',
        'Maximum': 'Maximum',
        'Dot': 'Dot',
        'Average': 'Average'
    }
    params = {'layer_type': eltwiseMap[layer.__class__.__name__]}
    return jsonLayer('Eltwise', params, layer)


# ********** Advanced Activations Layers **********
def LeakyReLU(layer):
    params = {'negative_slope': layer.alpha.tolist()}
    return jsonLayer('ReLU', params, layer)


def PReLU(layer):
    return jsonLayer('PReLU', {}, layer)


def ELU(layer):
    params = {'alpha': layer.alpha.tolist()}
    return jsonLayer('ELU', params, layer)


def ThresholdedReLU(layer):
    params = {'theta': layer.theta.tolist()}
    return jsonLayer('ThresholdedReLU', params, layer)


# ********** Normalisation Layers **********
def BatchNorm(layer):
    params = {}
    params['eps'] = layer.epsilon
    params['moving_average_fraction'] = layer.momentum
    params['moving_mean_initializer'] = layer.moving_mean_initializer.__class__.__name__
    params['moving_variance_initializer'] = layer.moving_variance_initializer.__class__.__name__
    return jsonLayer('BatchNorm', params, layer)


# ********** Noise Layers **********
def GaussianNoise(layer):
    params = {}
    params['stddev'] = layer.stddev
    return jsonLayer('GaussianNoise', params, layer)


def GaussianDropout(layer):
    params = {}
    params['rate'] = layer.rate
    return jsonLayer('GaussianDropout', params, layer)


def AlphaDropout(layer):
    params = {}
    params['rate'] = layer.rate
    if (layer.seed):
        params['seed'] = layer.seed
    return jsonLayer('AlphaDropout', params, layer)


# ********** Utility Layers **********
def Scale(layer):
    tempLayer = {}
    params = {}
    params['axis'] = layer.axis
    params['bias_term'] = layer.center
    params['scale'] = layer.scale
    params['filler'] = layer.gamma_initializer.__class__.__name__
    params['bias_filler'] = layer.beta_initializer.__class__.__name__
    if (layer.beta_regularizer):
        params['beta_regularizer'] = layer.beta_regularizer.__class__.__name__
    if (layer.gamma_regularizer):
        params['gamma_regularizer'] = layer.gamma_regularizer.__class__.__name__
    if (layer.beta_constraint):
        params['beta_constraint'] = layer.beta_constraint.__class__.__name__
    if (layer.gamma_constraint):
        params['gamma_constraint'] = layer.gamma_constraint.__class__.__name__
    tempLayer['inbound_nodes'] = [[[layer.name + layer.__class__.__name__]]]
    return jsonLayer('Scale', params, tempLayer)


def Padding(layer):
    pad = np.asarray(layer.padding)
    if (len(pad.shape) == 1):
        pad = [pad[0]]
    else:
        pad = pad[:, 0].tolist()
    params = {'pad': pad}
    return jsonLayer('Pad', params, layer)


def TimeDistributed(layer):
    return jsonLayer('TimeDistributed', {}, layer)


def Bidirectional(layer):
    params = {}
    params['merge_mode'] = layer.merge_mode
    return jsonLayer('Bidirectional', params, layer)


def lrn(layer):
    params = {}
    params['k'] = layer.k
    params['beta'] = layer.beta
    params['alpha'] = layer.alpha
    params['local_size'] = layer.n
    return jsonLayer('LRN', params, layer)


# ********** Helper functions **********

# padding logic following
# https://github.com/Yangqing/caffe2/blob/master/caffe2/proto/caffe2_legacy.proto
def get_padding(params, input_shape, output_shape, pad_type, type):
    k_w, k_h, k_d, s_w, s_h, s_d = params
    if (type == '1D'):
        if (pad_type == 'valid'):
            return 0
        else:
            pad_w = ((output_shape[1] - 1) * s_w + k_w - input_shape[1]) / 2
            return pad_w
    elif (type == '2D'):
        if (pad_type == 'valid'):
            return [0, 0]
        else:
            pad_h = ((output_shape[2] - 1) * s_h + k_h - input_shape[2]) / 2
            pad_w = ((output_shape[1] - 1) * s_w + k_w - input_shape[1]) / 2
            return (pad_h, pad_w)
    else:
        if (pad_type == 'valid'):
            return [0, 0, 0]
        else:
            pad_h = ((output_shape[2] - 1) * s_h + k_h - input_shape[2]) / 2
            pad_w = ((output_shape[1] - 1) * s_w + k_w - input_shape[1]) / 2
            pad_d = ((output_shape[3] - 1) * s_d + k_d - input_shape[3]) / 2
            return (pad_h, pad_w, pad_d)


def jsonLayer(type, params, layer):
    input = []
    if hasattr(layer, 'wrapped'):
        input.append(layer.wrapper[0])
    else:
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
