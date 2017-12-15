import caffe
from caffe import layers as L
import re


def get_iterable(x):
    return (x,)

# Weight/Bias filler mapping from Keras to Caffe,
# some which are not in Caffe were mapped to Xavier
fillerMap = {
    'Zeros': 'constant',
    'Ones': 'constant',
    'Constant': 'constant',
    'RandomNormal': 'uniform',
    'RandomUniform': 'gaussian',
    'TruncatedNormal': 'gaussian',
    'VarianceScaling': 'gaussian',
    'Orthogonal': 'xavier',
    'Identity': 'constant',
    'lecun_uniform': 'uniform',
    'glorot_normal': 'xavier',
    'glorot_uniform': 'xavier',
    'he_normal': 'msra',
    'he_uniform': 'msra'
}


def export_ImageData(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    transform_param = {}
    transform_param['scale'] = layerParams['scale']
    transform_param['mirror'] = layerParams['mirror']
    transform_param['crop_size'] = layerParams['crop_size']
    transform_param['force_color'] = layerParams['force_color']
    transform_param['force_gray'] = layerParams['force_gray']
    if (layerParams['mean_value'] != ''):
        transform_param['mean_value'] = map(int, layerParams['mean_value'].split(','))
    elif (layerParams['mean_file'] != ''):
        transform_param['mean_file'] = layerParams['mean_file']

    image_data_param = {}
    image_data_param['source'] = layerParams['source']
    image_data_param['batch_size'] = layerParams['batch_size']
    image_data_param['rand_skip'] = layerParams['rand_skip']
    image_data_param['shuffle'] = layerParams['shuffle']
    image_data_param['new_height'] = layerParams['new_height']
    image_data_param['new_width'] = layerParams['new_width']
    image_data_param['is_color'] = layerParams['is_color']
    image_data_param['root_folder'] = layerParams['root_folder']
    if layerPhase is not None:
        caffeLayer = get_iterable(L.ImageData(
            transform_param=transform_param,
            image_data_param=image_data_param,
            include={
                'phase': int(layerPhase)
            }))
        if int(layerPhase) == 0:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.ImageData(
                transform_param=transform_param,
                image_data_param=image_data_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_Data(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    transform_param = {}
    transform_param['scale'] = layerParams['scale']
    transform_param['mirror'] = layerParams['mirror']
    transform_param['crop_size'] = layerParams['crop_size']
    transform_param['force_color'] = layerParams['force_color']
    transform_param['force_gray'] = layerParams['force_gray']
    if (layerParams['mean_value'] != ''):
        transform_param['mean_value'] = map(int, layerParams['mean_value'].split(','))
    elif (layerParams['mean_file'] != ''):
        transform_param['mean_file'] = layerParams['mean_file']

    data_param = {}
    data_param['source'] = layerParams['source']
    data_param['batch_size'] = layerParams['batch_size']
    data_param['backend'] = layerParams['backend']
    if (data_param['backend'] == 'LEVELDB'):
        data_param['backend'] = 0
    elif (data_param['backend'] == 'LMDB'):
        data_param['backend'] = 1
    data_param['rand_skip'] = layerParams['rand_skip']
    data_param['prefetch'] = layerParams['prefetch']
    if layerPhase is not None:
        caffeLayer = get_iterable(L.Data(
            transform_param=transform_param,
            data_param=data_param,
            include={
                'phase': int(layerPhase)
            }))
        if int(layerPhase) == 0:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.Data(
                transform_param=transform_param,
                data_param=data_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_HDF5Data(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    hdf5_data_param = {}
    hdf5_data_param['source'] = layerParams['source']
    hdf5_data_param['batch_size'] = layerParams['batch_size']
    hdf5_data_param['shuffle'] = layerParams['shuffle']
    if layerPhase is not None:
        caffeLayer = get_iterable(L.HDF5Data(
            hdf5_data_param=hdf5_data_param,
            include={
                'phase': int(layerPhase)
            }))
        if int(layerPhase) == 0:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.HDF5Data(
                hdf5_data_param=hdf5_data_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_HDF5Output(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    hdf5_output_param = {'file_name': layerParams['file_name']}
    if layerPhase is not None:
        if int(layerPhase) == 0:
            caffeLayer = get_iterable(L.HDF5Output(
                *[ns_train[x] for x in blobNames[layerId]['bottom']],
                hdf5_output_param=hdf5_output_param,
                include={
                    'phase': int(layerPhase)
                }))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            caffeLayer = get_iterable(L.HDF5Output(
                *[ns_test[x] for x in blobNames[layerId]['bottom']],
                hdf5_output_param=hdf5_output_param,
                include={
                    'phase': int(layerPhase)
                }))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.HDF5Output(
                *[ns[x] for x in blobNames[layerId]['bottom']],
                hdf5_output_param=hdf5_output_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_Input(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    input_param = {'shape': {'dim': map(int, layerParams['dim'].split(','))}}
    for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.Input(
                input_param=input_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_WindowData(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    transform_param = {}
    transform_param['scale'] = layerParams['scale']
    transform_param['mirror'] = layerParams['mirror']
    transform_param['crop_size'] = layerParams['crop_size']
    transform_param['force_color'] = layerParams['force_color']
    transform_param['force_gray'] = layerParams['force_gray']
    if (layerParams['mean_value'] != ''):
        transform_param['mean_value'] = map(int, layerParams['mean_value'].split(','))
    elif (layerParams['mean_file'] != ''):
        transform_param['mean_file'] = layerParams['mean_file']

    window_data_param = {}
    window_data_param['source'] = layerParams['source']
    window_data_param['batch_size'] = layerParams['batch_size']
    window_data_param['fg_threshold'] = layerParams['fg_threshold']
    window_data_param['bg_threshold'] = layerParams['bg_threshold']
    window_data_param['fg_fraction'] = layerParams['fg_fraction']
    window_data_param['context_pad'] = layerParams['context_pad']
    window_data_param['crop_mode'] = layerParams['crop_mode']
    window_data_param['cache_images'] = layerParams['cache_images']
    window_data_param['root_folder'] = layerParams['root_folder']
    if layerPhase is not None:
        caffeLayer = get_iterable(L.WindowData(
            transform_param=transform_param,
            window_data_param=window_data_param,
            include={
                'phase': int(layerPhase)
            }))
        if int(layerPhase) == 0:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.WindowData(
                transform_param=transform_param,
                window_data_param=window_data_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_MemoryData(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    memory_data_param = {}
    memory_data_param['batch_size'] = layerParams['batch_size']
    memory_data_param['channels'] = layerParams['channels']
    memory_data_param['height'] = layerParams['height']
    memory_data_param['width'] = layerParams['width']
    if layerPhase is not None:
        caffeLayer = get_iterable(L.MemoryData(
            memory_data_param=memory_data_param,
            include={
                'phase': int(layerPhase)
            }))
        if int(layerPhase) == 0:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.MemoryData(
                memory_data_param=memory_data_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_DummyData(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    # Adding a default size
    dummy_data_param = {}
    dummy_data_param['shape'] = {'dim': map(int, layerParams['dim'].split(','))}
    dummy_data_param['data_filler'] = {'type': layerParams['type']}
    if layerPhase is not None:
        caffeLayer = get_iterable(L.DummyData(
            dummy_data_param=dummy_data_param,
            include={
                'phase': int(layerPhase)
            }))
        if int(layerPhase) == 0:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.DummyData(
                dummy_data_param=dummy_data_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_Convolution(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    convolution_param = {}
    if layerParams['kernel_h'] != '':
        convolution_param['kernel_h'] = int(float(layerParams['kernel_h']))
    if layerParams['kernel_w'] != '':
        convolution_param['kernel_w'] = int(float(layerParams['kernel_w']))
    if layerParams['stride_h'] != '':
        convolution_param['stride_h'] = int(float(layerParams['stride_h']))
    if layerParams['stride_w'] != '':
        convolution_param['stride_w'] = int(float(layerParams['stride_w']))
    if layerParams['num_output'] != '':
        convolution_param['num_output'] = int(float(layerParams['num_output']))
    if layerParams['pad_h'] != '':
        convolution_param['pad_h'] = int(float(layerParams['pad_h']))
    if layerParams['pad_w'] != '':
        convolution_param['pad_w'] = int(float(layerParams['pad_w']))
    if layerParams['weight_filler'] != '':
        convolution_param['weight_filler'] = {}
        try:
            convolution_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            convolution_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        convolution_param['bias_filler'] = {}
        try:
            convolution_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            convolution_param['bias_filler']['type'] = layerParams['bias_filler']
    convolution_param['dilation'] = layerParams['dilation_h']
    convolution_param['bias_term'] = layerParams['use_bias']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Convolution(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            convolution_param=convolution_param,
            param=[
                {
                    'lr_mult': 1
                },
                {
                    'lr_mult': 2
                }
            ]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Pooling(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    pooling_param = {}
    if layerParams['kernel_h'] != '':
        pooling_param['kernel_h'] = int(float(layerParams['kernel_h']))
    if layerParams['kernel_w'] != '':
        pooling_param['kernel_w'] = int(float(layerParams['kernel_w']))
    if layerParams['stride_h'] != '':
        pooling_param['stride_h'] = int(float(layerParams['stride_h']))
    if layerParams['stride_w'] != '':
        pooling_param['stride_w'] = int(float(layerParams['stride_w']))
    if layerParams['pad_h'] != '':
        pooling_param['pad_h'] = int(float(layerParams['pad_h']))
    if layerParams['pad_w'] != '':
        pooling_param['pad_w'] = int(float(layerParams['pad_w']))
    if layerParams['pool'] != '':
        pool = layerParams['pool']
        if(pool == 'MAX'):
            pool = 0
        elif(pool == 'AVE'):
            pool = 1
        elif(pool == 'STOCHASTIC'):
            pool = 2
        pooling_param['pool'] = pool
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Pooling(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            pooling_param=pooling_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Crop(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    crop_param = {}
    if layerParams['axis'] != '':
        crop_param['axis'] = int(float(layerParams['axis']))
    if layerParams['offset'] != '':
        crop_param['offset'] = int(float(layerParams['offset']))
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Crop(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            crop_param=crop_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_SPP(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    spp_param = {}
    spp_param['pool'] = layerParams['pool']
    spp_param['pyramid_height'] = layerParams['pyramid_height']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.SPP(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            spp_param=spp_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Deconvolution(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    convolution_param = {}
    if layerParams['kernel_h'] != '':
        convolution_param['kernel_h'] = int(float(layerParams['kernel_h']))
    if layerParams['kernel_w'] != '':
        convolution_param['kernel_w'] = int(float(layerParams['kernel_w']))
    if layerParams['stride_h'] != '':
        convolution_param['stride_h'] = int(float(layerParams['stride_h']))
    if layerParams['stride_w'] != '':
        convolution_param['stride_w'] = int(float(layerParams['stride_w']))
    if layerParams['num_output'] != '':
        convolution_param['num_output'] = int(float(layerParams['num_output']))
    if layerParams['pad_h'] != '':
        convolution_param['pad_h'] = int(float(layerParams['pad_h']))
    if layerParams['pad_w'] != '':
        convolution_param['pad_w'] = int(float(layerParams['pad_w']))
    if layerParams['weight_filler'] != '':
        convolution_param['weight_filler'] = {}
        try:
            convolution_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            convolution_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        convolution_param['bias_filler'] = {}
        try:
            convolution_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            convolution_param['bias_filler']['type'] = layerParams['bias_filler']
    convolution_param['dilation'] = layerParams['dilation_h']
    convolution_param['bias_term'] = layerParams['use_bias']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Deconvolution(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            convolution_param=convolution_param,
            param=[
                {
                    'lr_mult': 1
                },
                {
                    'lr_mult': 2
                }
            ]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Recurrent(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    recurrent_param = {}
    recurrent_param['num_output'] = int(layerParams['num_output'])
    if layerParams['weight_filler'] != '':
        recurrent_param['weight_filler'] = {}
        try:
            recurrent_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            recurrent_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        recurrent_param['bias_filler'] = {}
        try:
            recurrent_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            recurrent_param['bias_filler']['type'] = layerParams['bias_filler']
    recurrent_param['debug_info'] = layerParams['debug_info']
    recurrent_param['expose_hidden'] = layerParams['expose_hidden']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Recurrent(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            recurrent_param=recurrent_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_RNN(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    recurrent_param = {}
    recurrent_param['num_output'] = int(layerParams['num_output'])
    if layerParams['weight_filler'] != '':
        recurrent_param['weight_filler'] = {}
        try:
            recurrent_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            recurrent_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        recurrent_param['bias_filler'] = {}
        try:
            recurrent_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            recurrent_param['bias_filler']['type'] = layerParams['bias_filler']
    recurrent_param['debug_info'] = layerParams['debug_info']
    recurrent_param['expose_hidden'] = layerParams['expose_hidden']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.RNN(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            recurrent_param=recurrent_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_LSTM(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    recurrent_param = {}
    recurrent_param['num_output'] = int(layerParams['num_output'])
    if layerParams['weight_filler'] != '':
        recurrent_param['weight_filler'] = {}
        try:
            recurrent_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            recurrent_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        recurrent_param['bias_filler'] = {}
        try:
            recurrent_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            recurrent_param['bias_filler']['type'] = layerParams['bias_filler']
    recurrent_param['debug_info'] = layerParams['debug_info']
    recurrent_param['expose_hidden'] = layerParams['expose_hidden']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.LSTM(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            recurrent_param=recurrent_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_InnerProduct(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inner_product_param = {}
    if layerParams['num_output'] != '':
        inner_product_param['num_output'] = int(float(layerParams['num_output']))
    if layerParams['weight_filler'] != '':
        inner_product_param['weight_filler'] = {}
        try:
            inner_product_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            inner_product_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        inner_product_param['bias_filler'] = {}
        try:
            inner_product_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            inner_product_param['bias_filler']['type'] = layerParams['bias_filler']
    inner_product_param['bias_term'] = layerParams['use_bias']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.InnerProduct(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            inner_product_param=inner_product_param,
            param=[
                {
                    'lr_mult': 1
                },
                {
                    'lr_mult': 2
                }
            ]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Dropout(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    # inplace dropout? caffe-tensorflow do not work
    inplace = layerParams['inplace']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Dropout(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Embed(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    embed_param = {}
    if layerParams['num_output'] != '':
        embed_param['num_output'] = int(float(layerParams['num_output']))
    if layerParams['input_dim'] != '':
        embed_param['input_dim'] = int(float(layerParams['input_dim']))
    if layerParams['weight_filler'] != '':
        embed_param['weight_filler'] = {}
        try:
            embed_param['weight_filler']['type'] = \
                fillerMap[layerParams['weight_filler']]
        except:
            embed_param['weight_filler']['type'] = layerParams['weight_filler']
    if layerParams['bias_filler'] != '':
        embed_param['bias_filler'] = {}
        try:
            embed_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            embed_param['bias_filler']['type'] = layerParams['bias_filler']
    embed_param['bias_term'] = layerParams['bias_term']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Embed(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            embed_param=embed_param,
            param=[
                    {
                        'lr_mult': 1,
                        'decay_mult': 1
                    },
                    {
                        'lr_mult': 2,
                        'decay_mult': 0
                    }
                ]))
        # *([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_LRN(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    lrn_param = {}
    lrn_param['local_size'] = layerParams['local_size']
    lrn_param['alpha'] = layerParams['alpha']
    lrn_param['beta'] = layerParams['beta']
    lrn_param['k'] = layerParams['k']
    if(layerParams['norm_region'] == 'ACROSS_CHANNELS'):
        lrn_param['norm_region'] = 0
    else:
        lrn_param['norm_region'] = 1
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.LRN(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            lrn_param=lrn_param, in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_MVN(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    mvn_param = {}
    mvn_param['normalize_variance'] = layerParams['normalize_variance']
    mvn_param['across_channels'] = layerParams['across_channels']
    # JS converts 1e-9 to string
    mvn_param['eps'] = float(layerParams['eps'])
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.MVN(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            mvn_param=mvn_param, in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_BatchNorm(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    batch_norm_param = {}
    batch_norm_param['use_global_stats'] = layerParams['use_global_stats']
    batch_norm_param['moving_average_fraction'] = layerParams['moving_average_fraction']
    batch_norm_param['eps'] = float(layerParams['eps'])
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.BatchNorm(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            batch_norm_param=batch_norm_param, in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_ReLU(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    relu_param = {}
    relu_param['negative_slope'] = layerParams['negative_slope']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.ReLU(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, relu_param=relu_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_PReLU(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    prelu_param = {}
    prelu_param['channel_shared'] = layerParams['channel_shared']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.PReLU(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, prelu_param=prelu_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_ELU(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    elu_param = {}
    elu_param['alpha'] = layerParams['alpha']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.ELU(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, elu_param=elu_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Sigmoid(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Sigmoid(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_TanH(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.TanH(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_AbsVal(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.AbsVal(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Power(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    power_param = {}
    inplace = layerParams['inplace']
    power_param['power'] = layerParams['power']
    power_param['scale'] = layerParams['scale']
    power_param['shift'] = layerParams['shift']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Power(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, power_param=power_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Exp(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    exp_param = {}
    inplace = layerParams['inplace']
    exp_param['base'] = layerParams['base']
    exp_param['scale'] = layerParams['scale']
    exp_param['shift'] = layerParams['shift']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Exp(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, exp_param=exp_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Log(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    log_param = {}
    inplace = layerParams['inplace']
    log_param['base'] = layerParams['base']
    log_param['scale'] = layerParams['scale']
    log_param['shift'] = layerParams['shift']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Log(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, log_param=log_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_BNLL(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.BNLL(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Threshold(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    inplace = layerParams['inplace']
    threshold_param = {}
    threshold_param['threshold'] = layerParams['threshold']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Threshold(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            in_place=inplace, threshold_param=threshold_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Bias(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    bias_param = {}
    bias_param['axis'] = layerParams['axis']
    bias_param['num_axes'] = layerParams['num_axes']
    if layerParams['filler'] != '':
        bias_param['filler'] = {}
        try:
            bias_param['filler']['type'] = \
                fillerMap[layerParams['filler']]
        except:
            bias_param['filler']['type'] = layerParams['filler']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Bias(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            bias_param=bias_param
            ))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Scale(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    scale_param = {}
    scale_param['axis'] = layerParams['axis']
    scale_param['num_axes'] = layerParams['num_axes']
    if layerParams['filler'] != '':
        scale_param['filler'] = {}
        try:
            scale_param['filler']['type'] = \
                fillerMap[layerParams['filler']]
        except:
            scale_param['filler']['type'] = layerParams['filler']
    scale_param['bias_term'] = layerParams['bias_term']
    if layerParams['bias_filler'] != '':
        scale_param['bias_filler'] = {}
        try:
            scale_param['bias_filler']['type'] = \
                fillerMap[layerParams['bias_filler']]
        except:
            scale_param['bias_filler']['type'] = layerParams['bias_filler']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Scale(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            scale_param=scale_param
            ))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Flatten(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    flatten_param = {}
    flatten_param['axis'] = layerParams['axis']
    flatten_param['end_axis'] = layerParams['end_axis']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Flatten(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            flatten_param=flatten_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Reshape(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    reshape_param = {'shape': {'dim': map(int, layerParams['dim'].split(','))}}
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Reshape(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            reshape_param=reshape_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_BatchReindex(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.BatchReindex(
            *[ns[x] for x in blobNames[layerId]['bottom']]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Split(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Split(
            *[ns[x] for x in blobNames[layerId]['bottom']]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Concat(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Concat(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            ntop=len(blobNames[layerId]['top'])))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Slice(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    slice_param = {}
    slice_param['slice_point'] = map(int, layerParams['slice_point'].split(','))
    slice_param['axis'] = layerParams['axis']
    slice_param['slice_dim'] = layerParams['slice_dim']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Slice(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            slice_param=slice_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Eltwise(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    eltwise_param = {}
    if layerParams['layer_type'] != '':
        elt = layerParams['layer_type']
        if(elt == 'Product'):
            elt = 0
        elif(elt == 'Sum'):
            elt = 1
        elif(elt == 'Maximum'):
            elt = 2
    else:
        elt = 1  # Default is sum
    eltwise_param['operation'] = elt
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Eltwise(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            eltwise_param=eltwise_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Filter(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Filter(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            ntop=len(blobNames[layerId]['top'])))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


# This layer is currently not supported as there is no bottom blob
# def export_Parameter(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
#     parameter_param = {}
#     parameter_param['shape'] = map(int, layerParams['shape'].split(','))
#     for ns in (ns_train, ns_test):
#        caffeLayer = get_iterable(L.Parameter(
#            parameter_param=parameter_param))
#        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
#            ns[key] = value
#     return ns_train, ns_test


def export_Reduction(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    reduction_param = {}
    if(layerParams['operation'] == 'SUM'):
        reduction_param['operation'] = 1
    elif(layerParams['operation'] == 'ASUM'):
        reduction_param['operation'] = 2
    elif(layerParams['operation'] == 'SUMSQ'):
        reduction_param['operation'] = 3
    elif(layerParams['operation'] == 'MEAN'):
        reduction_param['operation'] = 4
    reduction_param['axis'] = layerParams['axis']
    reduction_param['coeff'] = layerParams['coeff']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Reduction(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            reduction_param=reduction_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Silence(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Silence(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            ntop=len(blobNames[layerId]['top'])))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_ArgMax(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    argmax_param = {}
    argmax_param['out_max_val'] = layerParams['out_max_val']
    argmax_param['top_k'] = layerParams['top_k']
    argmax_param['axis'] = layerParams['axis']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.ArgMax(
            *[ns[x] for x in blobNames[layerId]['bottom']],
            argmax_param=argmax_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Softmax(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.Softmax(
            *([ns[x] for x in blobNames[layerId]['bottom']])))
        # *([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_MultinomialLogisticLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.MultinomialLogisticLoss(
          *[ns[x] for x in blobNames[layerId]['bottom']]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_InfogainLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    infogain_loss_param = {}
    infogain_loss_param['source'] = layerParams['source']
    infogain_loss_param['axis'] = layerParams['axis']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.MultinomialLogisticLoss(
          *[ns[x] for x in blobNames[layerId]['bottom']],
          infogain_loss_param=infogain_loss_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_SoftmaxWithLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    softmax_param = {'axis': layerParams['axis']}
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.SoftmaxWithLoss(  # try L['SoftmaxWithLoss']
            *([ns[x] for x in blobNames[layerId]['bottom']]),
            softmax_param=softmax_param))
        # *([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_EuclideanLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.EuclideanLoss(
          *[ns[x] for x in blobNames[layerId]['bottom']]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_HingeLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    hinge_loss_param = {'norm': layerParams['norm']}
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.HingeLoss(
          *[ns[x] for x in blobNames[layerId]['bottom']],
          hinge_loss_param=hinge_loss_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_SigmoidCrossEntropyLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.SigmoidCrossEntropyLoss(
          *[ns[x] for x in blobNames[layerId]['bottom']]))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Accuracy(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    accuracy_param = {}
    accuracy_param['top_k'] = layerParams['top_k']
    accuracy_param['axis'] = layerParams['axis']
    if layerPhase is not None:
        if int(layerPhase) == 0:
            caffeLayer = get_iterable(L.Accuracy(
                *([ns_train[x] for x in blobNames[layerId]['bottom']]),
                accuracy_param=accuracy_param,
                # *([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label]),
                include={
                    'phase': int(layerPhase)
                }))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_train[key] = value
        elif int(layerPhase) == 1:
            caffeLayer = get_iterable(L.Accuracy(
                *([ns_test[x] for x in blobNames[layerId]['bottom']]),
                accuracy_param=accuracy_param,
                # *([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label]),
                include={
                    'phase': int(layerPhase)
                }))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns_test[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.Accuracy(
                *([ns[x] for x in blobNames[layerId]['bottom']]),
                accuracy_param=accuracy_param))
            # *([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


def export_ContrastiveLoss(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    contrastive_loss_param = {}
    contrastive_loss_param['margin'] = layerParams['margin']
    contrastive_loss_param['legacy_version'] = layerParams['legacy_version']
    for ns in (ns_train, ns_test):
        caffeLayer = get_iterable(L.ContrastiveLoss(
          *[ns[x] for x in blobNames[layerId]['bottom']],
          contrastive_loss_param=contrastive_loss_param))
        for key, value in zip(blobNames[layerId]['top'], caffeLayer):
            ns[key] = value
    return ns_train, ns_test


def export_Python(layerId, layerParams, layerPhase, ns_train, ns_test, blobNames):
    # Parameters not to be included in param_str
    notParamStr = ['module', 'layer', 'endPoint', 'loss_weight', 'dragDrop', 'param_str']
    hasParamStr = False
    python_param = {}
    python_param['module'] = layerParams['module']
    python_param['layer'] = layerParams['layer']
    for param in layerParams:
        if (param not in notParamStr):
            hasParamStr = True
            if 'param_str' not in python_param.keys():
                python_param['param_str'] = {}
            if isinstance(layerParams[param], str):
                try:
                    python_param['param_str'][param] = map(int,
                                                           layerParams[param].split(','))
                except:
                    python_param['param_str'][param] = layerParams[param]
            else:
                python_param['param_str'][param] = layerParams[param]
    if 'dragDrop' in layerParams.keys():
        python_param['param_str'] = layerParams['param_str']
    if (hasParamStr):
        python_param['param_str'] = str(python_param['param_str'])
    if 'loss_weight' in layerParams:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.Python(
              *[ns[x] for x in blobNames[layerId]['bottom']],
              python_param=python_param, loss_weight=layerParams['loss_weight']))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    else:
        for ns in (ns_train, ns_test):
            caffeLayer = get_iterable(L.Python(
              *[ns[x] for x in blobNames[layerId]['bottom']],
              python_param=python_param))
            for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                ns[key] = value
    return ns_train, ns_test


layer_map = {
    'ImageData': export_ImageData,
    'Data': export_Data,
    'HDF5Data': export_HDF5Data,
    'HDF5Output': export_HDF5Output,
    'Input': export_Input,
    'WindowData': export_WindowData,
    'MemoryData': export_MemoryData,
    'DummyData': export_DummyData,
    'Convolution': export_Convolution,
    'Pooling': export_Pooling,
    'Crop': export_Crop,
    'SPP': export_SPP,
    'Deconvolution': export_Deconvolution,
    'Recurrent': export_Recurrent,
    'RNN': export_RNN,
    'LSTM': export_LSTM,
    'InnerProduct': export_InnerProduct,
    'Dropout': export_Dropout,
    'Embed': export_Embed,
    'LRN': export_LRN,
    'MVN': export_MVN,
    'BatchNorm': export_BatchNorm,
    'ReLU': export_ReLU,
    'PReLU': export_PReLU,
    'ELU': export_ELU,
    'Sigmoid': export_Sigmoid,
    'TanH': export_TanH,
    'AbsVal': export_AbsVal,
    'Power': export_Power,
    'Exp': export_Exp,
    'Log': export_Log,
    'BNLL': export_BNLL,
    'Threshold': export_Threshold,
    'Bias': export_Bias,
    'Scale': export_Scale,
    'Flatten': export_Flatten,
    'Reshape': export_Reshape,
    'BatchReindex': export_BatchReindex,
    'Split': export_Split,
    'Concat': export_Concat,
    'Slice': export_Slice,
    'Eltwise': export_Eltwise,
    'Filter': export_Filter,
    # 'Parameter': export_Parameter,
    'Reduction': export_Reduction,
    'Silence': export_Silence,
    'ArgMax': export_ArgMax,
    'Softmax': export_Softmax,
    'MultinomialLogisticLoss': export_MultinomialLogisticLoss,
    'InfogainLoss': export_InfogainLoss,
    'SoftmaxWithLoss': export_SoftmaxWithLoss,
    'EuclideanLoss': export_EuclideanLoss,
    'HingeLoss': export_HingeLoss,
    'SigmoidCrossEntropyLoss': export_SigmoidCrossEntropyLoss,
    'Accuracy': export_Accuracy,
    'ContrastiveLoss': export_ContrastiveLoss,
    'Python': export_Python
}


def json_to_prototxt(net, net_name):
    # assumption: a layer can accept only one input blob
    # the data layer produces two blobs: data and label
    # the loss layer requires two blobs: <someData> and label
    # the label blob is hardcoded.
    # layers name have to be unique

    # custom DFS of the network
    input_dim = None

    stack = []
    layersProcessed = {}
    processOrder = []
    blobNames = {}
    for layerId in net:
        layersProcessed[layerId] = False
        blobNames[layerId] = {
            'bottom': [],
            'top': [],
        }
    blobId = 0

    def isProcessPossible(layerId):
        inputs = net[layerId]['connection']['input']
        for layerId in inputs:
            if layersProcessed[layerId] is False:
                return False
        return True

    # finding the data layer
    dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData']
    for layerId in net:
        if (net[layerId]['info']['type'] == 'Python'):
            if ('endPoint' not in net[layerId]['params'].keys()):
                net[layerId]['params']['dragDrop'] = True
                if (not net[layerId]['connection']['input']):
                    stack.append(layerId)
            else:
                if (net[layerId]['params']['endPoint'] == "1, 0"):
                    stack.append(layerId)
        if(net[layerId]['info']['type'] in dataLayers):
            stack.append(layerId)

    def changeTopBlobName(layerId, newName):
        blobNames[layerId]['top'] = newName

    while len(stack):

        i = len(stack) - 1

        while isProcessPossible(stack[i]) is False:
            i = i - 1

        layerId = stack[i]
        stack.remove(stack[i])

        inputs = net[layerId]['connection']['input']
        if len(inputs) > 0:
            if len(inputs) == 2 and (net[inputs[0]]['info']['phase'] is not None) \
                    and (net[inputs[1]]['info']['phase']):
                commonBlobName = blobNames[inputs[0]]['top']
                changeTopBlobName(inputs[1], commonBlobName)
                blobNames[layerId]['bottom'] = commonBlobName
            else:
                inputBlobNames = []
                for inputId in inputs:
                    inputBlobNames.extend(blobNames[inputId]['top'])
                blobNames[layerId]['bottom'] = inputBlobNames

        blobNames[layerId]['top'] = ['blob'+str(blobId)]
        blobId = blobId + 1

        for outputId in net[layerId]['connection']['output']:
            if outputId not in stack:
                stack.append(outputId)

        layersProcessed[layerId] = True
        processOrder.append(layerId)

    ns_train = caffe.NetSpec()
    ns_test = caffe.NetSpec()

    for layerId in processOrder:

        layer = net[layerId]
        layerParams = layer['params']
        layerType = layer['info']['type']
        layerPhase = layer['info']['phase']
        if (not layerParams['caffe']):
            if ('layer_type' in layerParams):
                raise Exception('Cannot export layer of type ' + layerType + ' ' + layerParams['layer_type']
                                + ' to Caffe.')
            else:
                raise Exception('Cannot export layer of type ' + layerType + ' to Caffe.')
        ns_train, ns_test = layer_map[layerType](layerId, layerParams, layerPhase,
                                                 ns_train, ns_test, blobNames)

    train = 'name: "' + net_name + '"\n' + str(ns_train.to_proto())
    test = str(ns_test.to_proto())

    # merge the train and test prototxt to get a single train_test prototxt
    testIndex = [m.start() for m in re.finditer('layer', test)]

    previousIndex = -1
    for i in range(len(testIndex)):
        if i < len(testIndex)-1:
            layer = test[testIndex[i]:testIndex[i+1]]
        else:
            layer = test[testIndex[i]:]
        a = train.find(layer)
        if a != -1:
            l = test[testIndex[previousIndex+1]:testIndex[i]]
            train = train[0:a]+l+train[a:]
            previousIndex = i
    if previousIndex < len(testIndex)-1:
        l = test[testIndex[previousIndex+1]:]
        train = train + l

    prototxt = train

    return prototxt, input_dim
