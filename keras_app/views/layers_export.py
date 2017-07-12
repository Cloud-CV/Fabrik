import numpy as np

from keras.layers import Dense, Activation, Dropout, Flatten, Reshape
from keras.layers import Conv2D, Conv2DTranspose, ZeroPadding2D
from keras.layers import MaxPooling2D, AveragePooling2D
from keras.layers import SimpleRNN, LSTM
from keras.layers import Embedding
from keras.layers import add, multiply, maximum, concatenate
from keras.layers.advanced_activations import LeakyReLU, PReLU, ELU
from keras.layers import BatchNormalization
from keras.layers import Input
from keras import regularizers


fillerMap = {
    'constant': 'Constant',
    'uniform': 'RandomUniform',
    'gaussian': 'RandomNormal',
    'xavier': 'glorot_normal',
    'msra': 'he_normal'
}

regularizerMap = {
    'l1': regularizers.l1(),
    'l2': regularizers.l2(),
    'l1_l2': regularizers.l1_l2(),
    'L1L2': regularizers.l1_l2(),
    'None': None
}

constraintMap = {
    'max_norm': 'max_norm',
    'non_neg': 'non_neg',
    'unit_norm': 'unit_norm',
    'MaxNorm': 'max_norm',
    'NonNeg': 'non_neg',
    'UnitNorm': 'unit_norm',
    'None': None
}


# ********** Data Layers **********
def data(layer, layer_in, layerId):
    out = {layerId: Input(layer['shape']['output'][1:]+layer['shape']['output'][:1])}
    return out


# ********** Vision Layers **********
def convolution(layer, layer_in, layerId):
    out = {}
    padding = get_padding(layer)
    k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
    s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
    d_h, d_w = layer['params']['dilation_h'], layer['params']['dilation_w']
    if (layer['params']['weight_filler'] in fillerMap):
        kernel_initializer = fillerMap[layer['params']['weight_filler']]
    else:
        kernel_initializer = layer['params']['weight_filler']
    if (layer['params']['bias_filler'] in fillerMap):
        bias_initializer = fillerMap[layer['params']['bias_filler']]
    else:
        bias_initializer = layer['params']['bias_filler']
    filters = layer['params']['num_output']
    if (padding == 'custom'):
        p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
        out[layerId + 'Pad'] = ZeroPadding2D(padding=(p_h, p_w))(*layer_in)
        padding = 'valid'
        layer_in = [out[layerId + 'Pad']]
    kernel_regularizer = regularizerMap[layer['params']['kernel_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    kernel_constraint = constraintMap[layer['params']['kernel_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    use_bias = layer['params']['use_bias']
    out[layerId] = Conv2D(filters, [k_h, k_w], strides=(s_h, s_w), padding=padding,
                          dilation_rate=(d_h, d_w), kernel_initializer=kernel_initializer,
                          bias_initializer=bias_initializer, kernel_regularizer=kernel_regularizer,
                          bias_regularizer=bias_regularizer,
                          activity_regularizer=activity_regularizer, use_bias=use_bias,
                          bias_constraint=bias_constraint, kernel_constraint=kernel_constraint)(
                          *layer_in)
    return out


def deconvolution(layer, layer_in, layerId):
    out = {}
    padding = get_padding(layer)
    k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
    s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
    d_h, d_w = layer['params']['dilation_h'], layer['params']['dilation_w']
    if (layer['params']['weight_filler'] in fillerMap):
        kernel_initializer = fillerMap[layer['params']['weight_filler']]
    else:
        kernel_initializer = layer['params']['weight_filler']
    if (layer['params']['bias_filler'] in fillerMap):
        bias_initializer = fillerMap[layer['params']['bias_filler']]
    else:
        bias_initializer = layer['params']['bias_filler']
    filters = layer['params']['num_output']
    if (padding == 'custom'):
        p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
        out[layerId + 'Pad'] = ZeroPadding2D(padding=(p_h, p_w))(*layer_in)
        padding = 'valid'
        layer_in = [out[layerId + 'Pad']]
    kernel_regularizer = regularizerMap[layer['params']['kernel_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    kernel_constraint = constraintMap[layer['params']['kernel_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    use_bias = layer['params']['use_bias']
    out[layerId] = Conv2DTranspose(filters, [k_h, k_w], strides=(s_h, s_w), padding=padding,
                                   dilation_rate=(d_h, d_w), kernel_initializer=kernel_initializer,
                                   bias_initializer=bias_initializer,
                                   kernel_regularizer=kernel_regularizer,
                                   bias_regularizer=bias_regularizer,
                                   activity_regularizer=activity_regularizer, use_bias=use_bias,
                                   bias_constraint=bias_constraint,
                                   kernel_constraint=kernel_constraint)(*layer_in)
    return out


def pooling(layer, layer_in, layerId):
    out = {}
    padding = get_padding(layer)
    k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
    s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
    if (padding == 'custom'):
        p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
        out[layerId + 'Pad'] = ZeroPadding2D(padding=(p_h, p_w))(layer_in)
        padding = 'valid'
        layer_in = out[layerId + 'Pad']
    if (layer['params']['pool'] == 1):
        out[layerId] = AveragePooling2D(pool_size=(k_h, k_w), strides=(s_h, s_w), padding=padding)(
                                        *layer_in)
    else:
        out[layerId] = MaxPooling2D(pool_size=(k_h, k_w), strides=(s_h, s_w), padding=padding)(
                                    *layer_in)
    return out


# ********** Common Layers **********
def dense(layer, layer_in, layerId):
    out = {}
    if (len(layer['shape']['input']) > 1):
        out[layerId + 'Flatten'] = Flatten()(*layer_in)
        layer_in = [out[layerId + 'Flatten']]
    units = layer['params']['num_output']
    if (layer['params']['weight_filler'] in fillerMap):
        kernel_initializer = fillerMap[layer['params']['weight_filler']]
    else:
        kernel_initializer = layer['params']['weight_filler']
    if (layer['params']['bias_filler'] in fillerMap):
        bias_initializer = fillerMap[layer['params']['bias_filler']]
    else:
        bias_initializer = layer['params']['bias_filler']
    kernel_regularizer = regularizerMap[layer['params']['kernel_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    kernel_constraint = constraintMap[layer['params']['kernel_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    use_bias = layer['params']['use_bias']
    out[layerId] = Dense(units=units, kernel_initializer=kernel_initializer,
                         kernel_regularizer=kernel_regularizer, bias_regularizer=bias_regularizer,
                         activity_regularizer=activity_regularizer, bias_constraint=bias_constraint,
                         kernel_constraint=kernel_constraint, use_bias=use_bias,
                         bias_initializer=bias_initializer)(*layer_in)
    return out


def dropout(layer, layer_in, layerId):
    out = {layerId: Dropout(0.5)(*layer_in)}
    return out


def embed(layer, layer_in, layerId):
    out = {}
    if (layer['params']['weight_filler'] in fillerMap):
        embeddings_initializer = fillerMap[layer['params']['weight_filler']]
    else:
        embeddings_initializer = layer['params']['weight_filler']
    embeddings_regularizer = regularizerMap[layer['params']['embeddings_regularizer']]
    embeddings_constraint = constraintMap[layer['params']['embeddings_constraint']]
    mask_zero = layer['params']['mask_zero']
    if (layer['params']['input_length']):
        input_length = layer['params']['input_length']
    else:
        input_length = None
    out[layerId] = Embedding(layer['params']['input_dim'], layer['params']['num_output'],
                             embeddings_initializer=embeddings_initializer,
                             embeddings_regularizer=embeddings_regularizer,
                             embeddings_constraint=embeddings_constraint,
                             mask_zero=mask_zero, input_length=input_length)(*layer_in)
    return out


# ********** Recurrent Layers **********
def recurrent(layer, layer_in, layerId):
    out = {}
    recurrentMap = {
        'RNN': SimpleRNN,
        'LSTM': LSTM
    }
    units = layer['params']['num_output']
    if (layer['params']['weight_filler'] in fillerMap):
        kernel_initializer = fillerMap[layer['params']['weight_filler']]
    else:
        kernel_initializer = layer['params']['weight_filler']
    if (layer['params']['bias_filler'] in fillerMap):
        bias_initializer = fillerMap[layer['params']['bias_filler']]
    else:
        bias_initializer = layer['params']['bias_filler']
    recurrent_initializer = layer['params']['recurrent_initializer']
    kernel_regularizer = regularizerMap[layer['params']['kernel_regularizer']]
    recurrent_regularizer = regularizerMap[layer['params']['recurrent_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    kernel_constraint = constraintMap[layer['params']['kernel_constraint']]
    recurrent_constraint = constraintMap[layer['params']['recurrent_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    use_bias = layer['params']['use_bias']
    dropout = layer['params']['dropout']
    recurrent_dropout = layer['params']['recurrent_dropout']
    out[layerId] = recurrentMap[layer['info']['type']](units, kernel_initializer=kernel_initializer,
                                                       bias_initializer=bias_initializer,
                                                       recurrent_initializer=recurrent_initializer,
                                                       kernel_regularizer=kernel_regularizer,
                                                       recurrent_regularizer=recurrent_regularizer,
                                                       bias_regularizer=bias_regularizer,
                                                       activity_regularizer=activity_regularizer,
                                                       kernel_constraint=kernel_constraint,
                                                       recurrent_constraint=recurrent_constraint,
                                                       bias_constraint=bias_constraint,
                                                       use_bias=use_bias, dropout=dropout,
                                                       recurrent_dropout=recurrent_dropout)(
                                                       *layer_in)
    return out


# ********** Normalisation Layers **********
def batchNorm(layer, layer_in, layerId, idNext, nextLayer,):
    out = {}
    momentum = layer['params']['moving_average_fraction']
    eps = layer['params']['eps']
    if (eps < 1e-5):
        eps = 0.0001  # In Keras the max epsilon allowed in 1e-5
    moving_mean_initializer = layer['params']['moving_mean_initializer']
    moving_variance_initializer = layer['params']['moving_variance_initializer']
    if (nextLayer['info']['type'] == 'Scale'):
        axis = nextLayer['params']['axis']
        center = nextLayer['params']['bias_term']
        scale = nextLayer['params']['scale']
        if (nextLayer['params']['filler'] in fillerMap):
            gamma_initializer = fillerMap[nextLayer['params']['filler']]
        else:
            gamma_initializer = nextLayer['params']['filler']
        if (nextLayer['params']['bias_filler'] in fillerMap):
            beta_initializer = fillerMap[nextLayer['params']['bias_filler']]
        else:
            beta_initializer = nextLayer['params']['bias_filler']
        gamma_regularizer = regularizerMap[nextLayer['params']['gamma_regularizer']]
        beta_regularizer = regularizerMap[nextLayer['params']['beta_regularizer']]
        gamma_constraint = constraintMap[nextLayer['params']['gamma_constraint']]
        beta_constraint = constraintMap[nextLayer['params']['beta_constraint']]
        out[idNext] = BatchNormalization(axis=axis, momentum=momentum, epsilon=eps,
                                         moving_mean_initializer=moving_mean_initializer,
                                         moving_variance_initializer=moving_variance_initializer,
                                         center=center, scale=scale,
                                         gamma_initializer=gamma_initializer,
                                         beta_initializer=beta_initializer,
                                         gamma_regularizer=gamma_regularizer,
                                         beta_regularizer=beta_regularizer,
                                         gamma_constraint=gamma_constraint,
                                         beta_constraint=beta_constraint)(*layer_in)
    else:
        out[layerId] = BatchNormalization(momentum=momentum, epsilon=eps,
                                          moving_mean_initializer=moving_mean_initializer,
                                          moving_variance_initializer=moving_variance_initializer,
                                          scale=False, center=False)(*layer_in)
    return out


# ********** Activation/Neuron Layers **********
def activation(layer, layer_in, layerId):
    out = {}
    if (layer['info']['type'] == 'ReLU'):
        if (layer['params']['negative_slope'] != 0):
            out[layerId] = LeakyReLU(alpha=layer['params']['negative_slope'])(*layer_in)
        else:
            out[layerId] = Activation('relu')(*layer_in)
    elif (layer['info']['type'] == 'PReLU'):
        out[layerId] = PReLU()(*layer_in)
    elif (layer['info']['type'] == 'ELU'):
        out[layerId] = ELU(alpha=layer['params']['alpha'])(*layer_in)
    elif (layer['info']['type'] == 'Sigmoid'):
        out[layerId] = Activation('sigmoid')(*layer_in)
    elif (layer['info']['type'] == 'TanH'):
        out[layerId] = Activation('tanh')(*layer_in)
    elif (layer['info']['type'] == 'Softmax'):
        out[layerId] = Activation('softmax')(*layer_in)
    return out


# ********** Utility Layers **********
def flatten(layer, layer_in, layerId):
    out = {layerId: Flatten()(*layer_in)}
    return out


def reshape(layer, layer_in, layerId):
    shape = map(int, layer['params']['dim'].split(','))
    out = {layerId: Reshape(shape[2:]+shape[1:2])(*layer_in)}
    return out


def concat(layer, layer_in, layerId):
    out = {layerId: concatenate(layer_in)}
    return out


def eltwise(layer, layer_in, layerId):
    out = {}
    if (layer['params']['operation'] == 0):
        # This input reverse is to handle visualization
        out[layerId] = multiply(layer_in[::-1])
    elif (layer['params']['operation'] == 1):
        out[layerId] = add(layer_in[::-1])
    else:
        out[layerId] = maximum(layer_in[::-1])
    return out


# logic as used in caffe-tensorflow
# https://github.com/ethereon/caffe-tensorflow/blob/master/kaffe/tensorflow/transformer.py
def get_padding(layer):
    if (layer['info']['type'] == 'Deconvolution'):
        _, i_h, i_w = layer['shape']['output']
        _, o_h, o_w = layer['shape']['input']
    else:
        _, i_h, i_w = layer['shape']['input']
        _, o_h, o_w = layer['shape']['output']
    k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
    s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
    s_o_h = np.ceil(i_h / float(s_h))
    s_o_w = np.ceil(i_w / float(s_w))
    if (o_h == s_o_h) and (o_w == s_o_w):
        return 'same'
    v_o_h = np.ceil((i_h - k_h + 1.0) / float(s_h))
    v_o_w = np.ceil((i_w - k_w + 1.0) / float(s_w))
    if (o_h == v_o_h) and (o_w == v_o_w):
        return 'valid'
    return 'custom'
