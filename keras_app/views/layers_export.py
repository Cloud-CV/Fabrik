import numpy as np

from keras.layers import Dense, Activation, Dropout, Flatten, Reshape, Permute, RepeatVector
from keras.layers import ActivityRegularization, Masking
from keras.layers import Conv1D, Conv2D, Conv3D, Conv2DTranspose
from keras.layers import UpSampling1D, UpSampling2D, UpSampling3D
from keras.layers import MaxPooling1D, MaxPooling2D, MaxPooling3D
from keras.layers import AveragePooling1D, AveragePooling2D, AveragePooling3D
from keras.layers import ZeroPadding1D, ZeroPadding2D, ZeroPadding3D
from keras.layers import LocallyConnected1D, LocallyConnected2D
from keras.layers import SimpleRNN, LSTM, GRU
from keras.layers import Embedding
from keras.layers import add, multiply, maximum, concatenate, average, dot
from keras.layers.advanced_activations import LeakyReLU, PReLU, ELU, ThresholdedReLU
from keras.layers import BatchNormalization
from keras.layers import GaussianNoise, GaussianDropout, AlphaDropout
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


# ********** Core Layers **********
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
    elif (layer['info']['type'] == 'ThresholdedReLU'):
        out[layerId] = ThresholdedReLU(theta=layer['params']['theta'])(*layer_in)
    elif (layer['info']['type'] == 'Sigmoid'):
        out[layerId] = Activation('sigmoid')(*layer_in)
    elif (layer['info']['type'] == 'TanH'):
        out[layerId] = Activation('tanh')(*layer_in)
    elif (layer['info']['type'] == 'Softmax'):
        out[layerId] = Activation('softmax')(*layer_in)
    elif (layer['info']['type'] == 'SELU'):
        out[layerId] = Activation('selu')(*layer_in)
    elif (layer['info']['type'] == 'Softplus'):
        out[layerId] = Activation('softplus')(*layer_in)
    elif (layer['info']['type'] == 'Softsign'):
        out[layerId] = Activation('softsign')(*layer_in)
    elif (layer['info']['type'] == 'HardSigmoid'):
        out[layerId] = Activation('hard_sigmoid')(*layer_in)
    return out


def dropout(layer, layer_in, layerId):
    out = {layerId: Dropout(0.5)(*layer_in)}
    return out


def flatten(layer, layer_in, layerId):
    out = {layerId: Flatten()(*layer_in)}
    return out


def reshape(layer, layer_in, layerId):
    shape = map(int, layer['params']['dim'].split(','))
    out = {layerId: Reshape(shape[2:]+shape[1:2])(*layer_in)}
    return out


def permute(layer, layer_in, layerId):
    out = {layerId: Permute(map(int, layer['params']['dim'].split(',')))(*layer_in)}
    return out


def repeat_vector(layer, layer_in, layerId):
    out = {layerId: RepeatVector(layer['params']['n'])(*layer_in)}
    return out


def regularization(layer, layer_in, layerId):
    l1 = layer['params']['l1']
    l2 = layer['params']['l2']
    out = {layerId: ActivityRegularization(l1=l1, l2=l2)(*layer_in)}
    return out


def masking(layer, layer_in, layerId):
    out = {layerId: Masking(mask_value=layer['params']['mask_value'])(*layer_in)}
    return out


# ********** Convolution Layers **********
def convolution(layer, layer_in, layerId):
    convMap = {
        '1D': Conv1D,
        '2D': Conv2D,
        '3D': Conv3D
    }
    out = {}
    padding = get_padding(layer)
    if (layer['params']['weight_filler'] in fillerMap):
        kernel_initializer = fillerMap[layer['params']['weight_filler']]
    else:
        kernel_initializer = layer['params']['weight_filler']
    if (layer['params']['bias_filler'] in fillerMap):
        bias_initializer = fillerMap[layer['params']['bias_filler']]
    else:
        bias_initializer = layer['params']['bias_filler']
    filters = layer['params']['num_output']
    kernel_regularizer = regularizerMap[layer['params']['kernel_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    kernel_constraint = constraintMap[layer['params']['kernel_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    use_bias = layer['params']['use_bias']
    layer_type = layer['params']['layer_type']
    if (layer_type == '1D'):
        strides = layer['params']['stride_w']
        kernel = layer['params']['kernel_w']
        dilation_rate = layer['params']['dilation_w']
        if (padding == 'custom'):
            p_w = layer['params']['pad_w']
            out[layerId + 'Pad'] = ZeroPadding1D(padding=p_w)(*layer_in)
            padding = 'valid'
            layer_in = [out[layerId + 'Pad']]
    elif (layer_type == '2D'):
        strides = (layer['params']['stride_h'], layer['params']['stride_w'])
        kernel = (layer['params']['kernel_h'], layer['params']['kernel_w'])
        dilation_rate = (layer['params']['dilation_h'], layer['params']['dilation_w'])
        if (padding == 'custom'):
            p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
            out[layerId + 'Pad'] = ZeroPadding2D(padding=(p_h, p_w))(*layer_in)
            padding = 'valid'
            layer_in = [out[layerId + 'Pad']]
    else:
        strides = (layer['params']['stride_h'], layer['params']['stride_w'],
                   layer['params']['stride_d'])
        kernel = (layer['params']['kernel_h'], layer['params']['kernel_w'],
                  layer['params']['kernel_d'])
        dilation_rate = (layer['params']['dilation_h'], layer['params']['dilation_w'],
                         layer['params']['dilation_d'])
        if (padding == 'custom'):
            p_h, p_w, p_d = layer['params']['pad_h'], layer['params']['pad_w'],\
                            layer['params']['pad_d']
            out[layerId + 'Pad'] = ZeroPadding3D(padding=(p_h, p_w, p_d))(*layer_in)
            padding = 'valid'
            layer_in = [out[layerId + 'Pad']]
    out[layerId] = convMap[layer_type](filters, kernel, strides=strides, padding=padding,
                                       dilation_rate=dilation_rate,
                                       kernel_initializer=kernel_initializer,
                                       bias_initializer=bias_initializer,
                                       kernel_regularizer=kernel_regularizer,
                                       bias_regularizer=bias_regularizer,
                                       activity_regularizer=activity_regularizer, use_bias=use_bias,
                                       bias_constraint=bias_constraint,
                                       kernel_constraint=kernel_constraint)(*layer_in)
    return out

# Separable Convolution is currently not supported with Theano backend
'''
def depthwiseConv(layer, layer_in, layerId):
    out = {}
    padding = get_padding(layer)
    filters = layer['params']['filters']
    k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
    s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
    depth_multiplier = layer['params']['depth_multiplier']
    use_bias = layer['params']['use_bias']
    depthwise_initializer = layer['params']['depthwise_initializer']
    pointwise_initializer = layer['params']['pointwise_initializer']
    bias_initializer = layer['params']['bias_initializer']
    if (padding == 'custom'):
        p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
        out[layerId + 'Pad'] = ZeroPadding2D(padding=(p_h, p_w))(*layer_in)
        padding = 'valid'
        layer_in = [out[layerId + 'Pad']]
    depthwise_regularizer = regularizerMap[layer['params']['depthwise_regularizer']]
    pointwise_regularizer = regularizerMap[layer['params']['pointwise_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    depthwise_constraint = constraintMap[layer['params']['depthwise_constraint']]
    pointwise_constraint = constraintMap[layer['params']['pointwise_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    out[layerId] = SeparableConv2D(filters, [k_h, k_w], strides=(s_h, s_w), padding=padding,
                                   depth_multiplier=depth_multiplier, use_bias=use_bias,
                                   depthwise_initializer=depthwise_initializer,
                                   pointwise_initializer=pointwise_initializer,
                                   bias_initializer=bias_initializer,
                                   depthwise_regularizer=depthwise_regularizer,
                                   pointwise_regularizer=pointwise_regularizer,
                                   bias_regularizer=bias_regularizer,
                                   activity_regularizer=activity_regularizer,
                                   depthwise_constraint=depthwise_constraint,
                                   pointwise_constraint=pointwise_constraint,
                                   bias_constraint=bias_constraint,)(*layer_in)
    return out'''


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


def upsample(layer, layer_in, layerId):
    upsampleMap = {
        '1D': UpSampling1D,
        '2D': UpSampling2D,
        '3D': UpSampling3D
    }
    out = {}
    layer_type = layer['params']['layer_type']
    if (layer_type == '1D'):
        size = layer['params']['size_w']
    elif (layer_type == '2D'):
        size = (layer['params']['size_h'], layer['params']['size_w'])
    else:
        size = (layer['params']['size_h'], layer['params']['size_w'],
                layer['params']['size_d'])
    out[layerId] = upsampleMap[layer_type](size=size)(*layer_in)
    return out


# ********** Pooling Layers **********
def pooling(layer, layer_in, layerId):
    poolMap = {
        ('1D', 'MAX'): MaxPooling1D,
        ('2D', 'MAX'): MaxPooling2D,
        ('3D', 'MAX'): MaxPooling3D,
        ('1D', 'AVE'): AveragePooling1D,
        ('2D', 'AVE'): AveragePooling2D,
        ('3D', 'AVE'): AveragePooling3D,
    }
    out = {}
    layer_type = layer['params']['layer_type']
    pool_type = layer['params']['pool']
    padding = get_padding(layer)
    if (layer_type == '1D'):
        strides = layer['params']['stride_w']
        kernel = layer['params']['kernel_w']
        if (padding == 'custom'):
            p_w = layer['params']['pad_w']
            out[layerId + 'Pad'] = ZeroPadding1D(padding=p_w)(*layer_in)
            padding = 'valid'
            layer_in = [out[layerId + 'Pad']]
    elif (layer_type == '2D'):
        strides = (layer['params']['stride_h'], layer['params']['stride_w'])
        kernel = (layer['params']['kernel_h'], layer['params']['kernel_w'])
        if (padding == 'custom'):
            p_h, p_w = layer['params']['pad_h'], layer['params']['pad_w']
            out[layerId + 'Pad'] = ZeroPadding2D(padding=(p_h, p_w))(*layer_in)
            padding = 'valid'
            layer_in = [out[layerId + 'Pad']]
    else:
        strides = (layer['params']['stride_h'], layer['params']['stride_w'],
                   layer['params']['stride_d'])
        kernel = (layer['params']['kernel_h'], layer['params']['kernel_w'],
                  layer['params']['kernel_d'])
        if (padding == 'custom'):
            p_h, p_w, p_d = layer['params']['pad_h'], layer['params']['pad_w'],\
                            layer['params']['pad_d']
            out[layerId + 'Pad'] = ZeroPadding3D(padding=(p_h, p_w, p_d))(*layer_in)
            padding = 'valid'
            layer_in = [out[layerId + 'Pad']]
    out[layerId] = poolMap[(layer_type, pool_type)](pool_size=kernel, strides=strides, padding=padding)(
                                                    *layer_in)
    return out


# ********** Locally-connected Layers **********
def locally_connected(layer, layer_in, layerId):
    localMap = {
        '1D': LocallyConnected1D,
        '2D': LocallyConnected2D,
    }
    out = {}
    kernel_initializer = layer['params']['kernel_initializer']
    bias_initializer = layer['params']['bias_initializer']
    filters = layer['params']['filters']
    kernel_regularizer = regularizerMap[layer['params']['kernel_regularizer']]
    bias_regularizer = regularizerMap[layer['params']['bias_regularizer']]
    activity_regularizer = regularizerMap[layer['params']['activity_regularizer']]
    kernel_constraint = constraintMap[layer['params']['kernel_constraint']]
    bias_constraint = constraintMap[layer['params']['bias_constraint']]
    use_bias = layer['params']['use_bias']
    layer_type = layer['params']['layer_type']
    if (layer_type == '1D'):
        strides = layer['params']['stride_w']
        kernel = layer['params']['kernel_w']
    else:
        strides = (layer['params']['stride_h'], layer['params']['stride_w'])
        kernel = (layer['params']['kernel_h'], layer['params']['kernel_w'])
    out[layerId] = localMap[layer_type](filters, kernel, strides=strides, padding='valid',
                                        kernel_initializer=kernel_initializer,
                                        bias_initializer=bias_initializer,
                                        kernel_regularizer=kernel_regularizer,
                                        bias_regularizer=bias_regularizer,
                                        activity_regularizer=activity_regularizer, use_bias=use_bias,
                                        bias_constraint=bias_constraint,
                                        kernel_constraint=kernel_constraint)(*layer_in)
    return out


# ********** Recurrent Layers **********
def recurrent(layer, layer_in, layerId):
    out = {}
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
    if ('return_sequences' in layer['params']):
        return_sequences = layer['params']['return_sequences']
    else:
        return_sequences = False
    if (layer['info']['type'] == 'GRU'):
        recurrent_activation = layer['params']['recurrent_activation']
        out[layerId] = GRU(units, kernel_initializer=kernel_initializer,
                           bias_initializer=bias_initializer,
                           recurrent_activation=recurrent_activation,
                           recurrent_initializer=recurrent_initializer,
                           kernel_regularizer=kernel_regularizer,
                           recurrent_regularizer=recurrent_regularizer,
                           bias_regularizer=bias_regularizer, activity_regularizer=activity_regularizer,
                           kernel_constraint=kernel_constraint, recurrent_constraint=recurrent_constraint,
                           bias_constraint=bias_constraint, use_bias=use_bias, dropout=dropout,
                           recurrent_dropout=recurrent_dropout)(*layer_in)
    elif (layer['info']['type'] == 'LSTM'):
        recurrent_activation = layer['params']['recurrent_activation']
        unit_forget_bias = layer['params']['unit_forget_bias']
        out[layerId] = LSTM(units, kernel_initializer=kernel_initializer,
                            bias_initializer=bias_initializer,
                            recurrent_activation=recurrent_activation, unit_forget_bias=unit_forget_bias,
                            recurrent_initializer=recurrent_initializer,
                            kernel_regularizer=kernel_regularizer,
                            recurrent_regularizer=recurrent_regularizer,
                            bias_regularizer=bias_regularizer, activity_regularizer=activity_regularizer,
                            kernel_constraint=kernel_constraint, recurrent_constraint=recurrent_constraint,
                            bias_constraint=bias_constraint, use_bias=use_bias, dropout=dropout,
                            recurrent_dropout=recurrent_dropout, return_sequences=return_sequences)(*layer_in)
    else:
        out[layerId] = SimpleRNN(units, kernel_initializer=kernel_initializer,
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
                                 recurrent_dropout=recurrent_dropout)(*layer_in)
    return out


# ********** Embedding Layers **********
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


# ********** Merge Layers **********
def eltwise(layer, layer_in, layerId):
    out = {}
    if (layer['params']['layer_type'] == 'Multiply'):
        # This input reverse is to handle visualization
        out[layerId] = multiply(layer_in[::-1])
    elif (layer['params']['layer_type'] == 'Sum'):
        out[layerId] = add(layer_in[::-1])
    elif (layer['params']['layer_type'] == 'Average'):
        out[layerId] = average(layer_in[::-1])
    elif (layer['params']['layer_type'] == 'Dot'):
        out[layerId] = dot(layer_in[::-1], -1)
    else:
        out[layerId] = maximum(layer_in[::-1])
    return out


def concat(layer, layer_in, layerId):
    out = {layerId: concatenate(layer_in)}
    return out


# ********** Noise Layers **********
def gaussian_noise(layer, layer_in, layerId):
    stddev = layer['params']['stddev']
    out = {layerId: GaussianNoise(stddev=stddev)(*layer_in)}
    return out


def gaussian_dropout(layer, layer_in, layerId):
    rate = layer['params']['rate']
    out = {layerId: GaussianDropout(rate=rate)(*layer_in)}
    return out


def alpha_dropout(layer, layer_in, layerId):
    rate = layer['params']['rate']
    seed = layer['params']['seed']
    out = {layerId: AlphaDropout(rate=rate, seed=seed)(*layer_in)}
    return out


# ********** Normalisation Layers **********
def batch_norm(layer, layer_in, layerId, idNext, nextLayer,):
    out = {}
    momentum = layer['params']['moving_average_fraction']
    eps = float(layer['params']['eps'])
    if (eps <= 1e-5):
        eps = 1e-4  # In Keras the smallest epsilon allowed is 1e-5
    moving_mean_initializer = layer['params']['moving_mean_initializer']
    moving_variance_initializer = layer['params']['moving_variance_initializer']
    if (nextLayer['info']['type'] == 'Scale'):
        axis = nextLayer['params']['axis']
        # In Caffe the first dimension has number of filters/outputs but in Keras it is the last
        # dimension
        if (axis == 1):
            axis = -1
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


# logic as used in caffe-tensorflow
# https://github.com/ethereon/caffe-tensorflow/blob/master/kaffe/tensorflow/transformer.py
def get_padding(layer):
    if (layer['info']['type'] == 'Deconvolution'):
        _, i_h, i_w = layer['shape']['output']
        _, o_h, o_w = layer['shape']['input']
        k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
        s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
        layer['params']['layer_type'] = '2D'
    else:
        if (layer['params']['layer_type'] == '1D'):
            i_w = layer['shape']['input'][0]
            o_w = layer['shape']['output'][1]
            k_w = layer['params']['kernel_w']
            s_w = layer['params']['stride_w']

        elif (layer['params']['layer_type'] == '2D'):
            _, i_h, i_w = layer['shape']['input']
            _, o_h, o_w = layer['shape']['output']
            k_h, k_w = layer['params']['kernel_h'], layer['params']['kernel_w']
            s_h, s_w = layer['params']['stride_h'], layer['params']['stride_w']
        else:
            _, i_h, i_w, i_d = layer['shape']['input']
            _, o_h, o_w, o_d = layer['shape']['output']
            k_h, k_w, k_d = layer['params']['kernel_h'], layer['params']['kernel_w'],\
                layer['params']['kernel_d']
            s_h, s_w, s_d = layer['params']['stride_h'], layer['params']['stride_w'],\
                layer['params']['stride_d']
    if (layer['params']['layer_type'] == '1D'):
        s_o_w = np.ceil(i_w / float(s_w))
        if (o_w == s_o_w):
            return 'same'
        v_o_w = np.ceil((i_w - k_w + 1.0) / float(s_w))
        if (o_w == v_o_w):
            return 'valid'
        return 'custom'
    elif (layer['params']['layer_type'] == '2D'):
        s_o_h = np.ceil(i_h / float(s_h))
        s_o_w = np.ceil(i_w / float(s_w))
        if (o_h == s_o_h) and (o_w == s_o_w):
            return 'same'
        v_o_h = np.ceil((i_h - k_h + 1.0) / float(s_h))
        v_o_w = np.ceil((i_w - k_w + 1.0) / float(s_w))
        if (o_h == v_o_h) and (o_w == v_o_w):
            return 'valid'
        return 'custom'
    else:
        s_o_h = np.ceil(i_h / float(s_h))
        s_o_w = np.ceil(i_w / float(s_w))
        s_o_d = np.ceil(i_d / float(s_d))
        if (o_h == s_o_h) and (o_w == s_o_w) and (o_d == s_o_d):
            return 'same'
        v_o_h = np.ceil((i_h - k_h + 1.0) / float(s_h))
        v_o_w = np.ceil((i_w - k_w + 1.0) / float(s_w))
        v_o_d = np.ceil((i_d - k_d + 1.0) / float(s_d))
        if (o_h == v_o_h) and (o_w == v_o_w) and (o_d == v_o_d):
            return 'valid'
        return 'custom'
