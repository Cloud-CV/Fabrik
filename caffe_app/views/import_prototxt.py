from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
from caffe.proto import caffe_pb2
from google.protobuf import text_format


# ******Data Layers******
def ImageData(layer):
    params = {}
    params['source'] = layer.image_data_param.source
    params['batch_size'] = layer.image_data_param.batch_size
    params['rand_skip'] = layer.image_data_param.rand_skip
    params['shuffle'] = layer.image_data_param.shuffle
    params['new_height'] = layer.image_data_param.new_height
    params['new_width'] = layer.image_data_param.new_width
    params['is_color'] = layer.image_data_param.is_color
    params['root_folder'] = layer.image_data_param.root_folder
    return params


def Data(layer):
    params = {}
    params['source'] = layer.data_param.source
    params['batch_size'] = layer.data_param.batch_size
    params['backend'] = layer.data_param.backend
    if (params['backend'] == 0):
        params['backend'] = 'LEVELDB'
    else:
        params['backend'] = 'LMDB'
    params['rand_skip'] = layer.data_param.rand_skip
    params['prefetch'] = layer.data_param.prefetch
    return params


def HDF5Data(layer):
    params = {}
    params['source'] = layer.hdf5_data_param.source
    params['batch_size'] = layer.hdf5_data_param.batch_size
    params['shuffle'] = layer.hdf5_data_param.shuffle
    return params


def HDF5Output(layer):
    params = {}
    params['file_name'] = layer.hdf5_output_param.file_name
    return params


def Input(layer):
    params = {}
    params['dim'] = str(map(int, layer.input_param.shape[0].dim))[1:-1]
    return params


def WindowData(layer):
    params = {}
    params['source'] = layer.window_data_param.source
    params['batch_size'] = layer.window_data_param.batch_size
    params['fg_threshold'] = layer.window_data_param.fg_threshold
    params['bg_threshold'] = layer.window_data_param.bg_threshold
    params['fg_fraction'] = layer.window_data_param.fg_fraction
    params['context_pad'] = layer.window_data_param.context_pad
    params['crop_mode'] = layer.window_data_param.crop_mode
    params['cache_images'] = layer.window_data_param.cache_images
    params['root_folder'] = layer.window_data_param.root_folder
    return params


def MemoryData(layer):
    params = {}
    params['batch_size'] = layer.memory_data_param.batch_size
    params['channels'] = layer.memory_data_param.channels
    params['height'] = layer.memory_data_param.height
    params['width'] = layer.memory_data_param.width
    return params


def DummyData(layer):
    params = {}
    params['dim'] = str(map(int, layer.dummy_data_param.shape[0].dim))[1:-1]
    params['type'] = str(layer.dummy_data_param.data_filler[0].type)
    return params


# ********** Vision Layers **********
def Convolution(layer):
    params = {}
    if len(layer.convolution_param.kernel_size):
        params['kernel_h'] = layer.convolution_param.kernel_size[0]
        params['kernel_w'] = layer.convolution_param.kernel_size[0]
    if layer.convolution_param.kernel_w:
        params['kernel_w'] = layer.convolution_param.kernel_w
    if layer.convolution_param.kernel_h:
        params['kernel_h'] = layer.convolution_param.kernel_h
    if len(layer.convolution_param.pad):
        params['pad_h'] = layer.convolution_param.pad[0]
        params['pad_w'] = layer.convolution_param.pad[0]
    if layer.convolution_param.pad_w:
        params['pad_w'] = layer.convolution_param.pad_w
    if layer.convolution_param.pad_h:
        params['pad_h'] = layer.convolution_param.pad_h
    if len(layer.convolution_param.stride):
        params['stride_h'] = layer.convolution_param.stride_h \
            or layer.convolution_param.stride[0]
        params['stride_w'] = layer.convolution_param.stride_w \
            or layer.convolution_param.stride[0]
    if len(layer.convolution_param.dilation):
        params['dilation_h'] = layer.convolution_param.dilation[0]
        params['dilation_w'] = layer.convolution_param.dilation[0]
    params['weight_filler'] = layer.convolution_param.weight_filler.type
    params['bias_filler'] = layer.convolution_param.bias_filler.type
    params['num_output'] = layer.convolution_param.num_output
    params['use_bias'] = layer.convolution_param.bias_term
    params['layer_type'] = '2D'
    return params


def Pooling(layer):
    params = {}
    params['pad_h'] = layer.pooling_param.pad_h or layer.pooling_param.pad
    params['pad_w'] = layer.pooling_param.pad_w or layer.pooling_param.pad
    params['stride_h'] = layer.pooling_param.stride_h or layer.pooling_param.stride
    params['stride_w'] = layer.pooling_param.stride_w or layer.pooling_param.stride
    params['kernel_h'] = layer.pooling_param.kernel_h or layer.pooling_param.kernel_size
    params['kernel_w'] = layer.pooling_param.kernel_w or layer.pooling_param.kernel_size
    params['pool'] = layer.pooling_param.pool
    if (params['pool'] == 0):
        params['pool'] = 'MAX'
    elif (params['pool'] == 1):
        params['pool'] = 'AVE'
    else:
        params['pool'] = 'STOCHASTIC'
    params['layer_type'] = '2D'
    return params


def SPP(layer):
    params = {}
    params['pool'] = layer.spp_param.pool
    params['pyramid_height'] = layer.spp_param.pyramid_height
    return params


def Crop(layer):
    params = {}
    if layer.crop_param.axis:
        params['axis'] = layer.crop_param.axis
    if len(layer.crop_param.offset):
        params['offset'] = layer.crop_param.offset[0]
    return params


def Deconvolution(layer):
    params = {}
    if len(layer.convolution_param.kernel_size):
        params['kernel_h'] = layer.convolution_param.kernel_size[0]
        params['kernel_w'] = layer.convolution_param.kernel_size[0]
    if layer.convolution_param.kernel_w:
        params['kernel_w'] = layer.convolution_param.kernel_w
    if layer.convolution_param.kernel_h:
        params['kernel_h'] = layer.convolution_param.kernel_h
    if len(layer.convolution_param.pad):
        params['pad_h'] = layer.convolution_param.pad[0]
        params['pad_w'] = layer.convolution_param.pad[0]
    if layer.convolution_param.pad_w:
        params['pad_w'] = layer.convolution_param.pad_w
    if layer.convolution_param.pad_h:
        params['pad_h'] = layer.convolution_param.pad_h
    if len(layer.convolution_param.stride):
        params['stride_h'] = layer.convolution_param.stride_h \
            or layer.convolution_param.stride[0]
        params['stride_w'] = layer.convolution_param.stride_w \
            or layer.convolution_param.stride[0]
    if len(layer.convolution_param.dilation):
        params['dilation_h'] = layer.convolution_param.dilation[0]
        params['dilation_w'] = layer.convolution_param.dilation[0]
    params['weight_filler'] = layer.convolution_param.weight_filler.type
    params['bias_filler'] = layer.convolution_param.bias_filler.type
    params['num_output'] = layer.convolution_param.num_output
    params['use_bias'] = layer.convolution_param.bias_term
    return params


# ********** Recurrent Layers **********
def Recurrent(layer):
    params = {}
    params['num_output'] = layer.recurrent_param.num_output
    params['weight_filler'] = layer.recurrent_param.weight_filler.type
    params['bias_filler'] = layer.recurrent_param.bias_filler.type
    params['debug_info'] = layer.recurrent_param.debug_info
    params['expose_hidden'] = layer.recurrent_param.expose_hidden
    return params


# ********** Common Layers **********
def InnerProduct(layer):
    params = {}
    params['num_output'] = layer.inner_product_param.num_output
    params['weight_filler'] = layer.inner_product_param.weight_filler.type
    params['bias_filler'] = layer.inner_product_param.bias_filler.type
    params['use_bias'] = layer.inner_product_param.bias_term
    return params


def Dropout(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    return params


def Embed(layer):
    params = {}
    params['bias_term'] = layer.embed_param.bias_term
    params['input_dim'] = layer.embed_param.input_dim
    params['num_output'] = layer.embed_param.num_output
    params['weight_filler'] = layer.embed_param.weight_filler.type
    params['bias_filler'] = layer.embed_param.bias_filler.type
    return params


# ********** Normalisation Layers **********
def LRN(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['local_size'] = layer.lrn_param.local_size
    params['alpha'] = layer.lrn_param.alpha
    params['beta'] = layer.lrn_param.beta
    params['k'] = layer.lrn_param.k
    if layer.lrn_param.norm_region:
        params['norm_region'] = layer.lrn_param.norm_region
    else:
        params['norm_region'] = 'ACROSS_CHANNELS'
    return params


def MVN(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['normalize_variance'] = layer.mvn_param.normalize_variance
    params['across_channels'] = layer.mvn_param.across_channels
    params['eps'] = layer.mvn_param.eps
    return params


def BatchNorm(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['use_global_stats'] = layer.batch_norm_param.use_global_stats
    params['moving_average_fraction'] = layer.batch_norm_param.moving_average_fraction
    params['eps'] = layer.batch_norm_param.eps
    return params


# ********** Activation/Neuron Layers **********
def ReLU(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['negative_slope'] = layer.relu_param.negative_slope
    return params


def PReLU(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['channel_shared'] = layer.prelu_param.channel_shared
    return params


def ELU(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['alpha'] = layer.elu_param.alpha
    return params


def Sigmoid(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    return params


def TanH(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    return params


def AbsVal(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    return params


def Power(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['power'] = layer.power_param.power
    params['scale'] = layer.power_param.scale
    params['shift'] = layer.power_param.shift
    return params


def Exp(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['base'] = layer.exp_param.base
    params['scale'] = layer.exp_param.scale
    params['shift'] = layer.exp_param.shift
    return params


def Log(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['base'] = layer.log_param.base
    params['scale'] = layer.log_param.scale
    params['shift'] = layer.log_param.shift
    return params


def BNLL(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    return params


def Threshold(layer):
    params = {}
    if(layer.top == layer.bottom):
        params['inplace'] = True
    params['threshold'] = layer.threshold_param.threshold
    return params


def Bias(layer):
    params = {}
    params['axis'] = layer.bias_param.axis
    params['num_axes'] = layer.bias_param.num_axes
    params['filler'] = layer.bias_param.filler.type
    return params


def Scale(layer):
    params = {}
    params['scale'] = True
    params['axis'] = layer.scale_param.axis
    params['num_axes'] = layer.scale_param.num_axes
    params['filler'] = layer.scale_param.filler.type
    params['bias_term'] = layer.scale_param.bias_term
    params['bias_filler'] = layer.scale_param.bias_filler.type
    return params


# ********** Utility Layers **********
def Flatten(layer):
    params = {}
    params['axis'] = layer.flatten_param.axis
    params['end_axis'] = layer.flatten_param.end_axis
    return params


def Reshape(layer):
    params = {}
    params['dim'] = str(map(int, layer.reshape_param.shape.dim))[1:-1]
    return params


def Slice(layer):
    params = {}
    params['slice_point'] = str(map(int, layer.slice_param.slice_point))[1:-1]
    params['axis'] = layer.slice_param.axis
    params['slice_dim'] = layer.slice_param.slice_dim
    return params


def Eltwise(layer):
    params = {}
    opMap = {
        0: 'Product',
        1: 'Sum',
        2: 'Maximum'
    }
    if layer.eltwise_param.operation:
        params['layer_type'] = opMap[layer.eltwise_param.operation]
    else:
        params['layer_type'] = 'Sum'
    return params


def Reduction(layer):
    params = {}
    if layer.reduction_param.operation:
        params['operation'] = layer.reduction_param.operation
        if (params['operation'] == 1):
            params['operation'] = 'SUM'
        elif (params['operation'] == 2):
            params['operation'] = 'ASUM'
        elif (params['operation'] == 3):
            params['operation'] = 'SUMSQ'
        else:
            params['operation'] = 'MEAN'
    else:
        params['operation'] = 'SUM'
    params['axis'] = layer.reduction_param.axis
    params['coeff'] = layer.reduction_param.coeff
    return params


def ArgMax(layer):
    params = {}
    params['out_max_val'] = layer.argmax_param.out_max_val
    params['top_k'] = layer.argmax_param.top_k
    params['axis'] = layer.argmax_param.axis
    return params


# ********** Loss Layers **********
def InfogainLoss(layer):
    params = {}
    params['source'] = layer.infogain_loss_param.source
    params['axis'] = layer.infogain_loss_param.axis
    return params


def SoftmaxWithLoss(layer):
    params = {}
    params['axis'] = layer.softmax_param.axis
    return params


def HingeLoss(layer):
    params = {}
    params['norm'] = layer.hinge_loss_param.norm
    return params


def Accuracy(layer):
    params = {}
    params['top_k'] = layer.accuracy_param.top_k
    params['axis'] = layer.accuracy_param.axis
    return params


def ContrastiveLoss(layer):
    params = {}
    params['margin'] = layer.contrastive_loss_param.margin
    params['legacy_version'] = layer.contrastive_loss_param.legacy_version
    return params


# ********** Python Layer **********
def Python(layer):
    params = {}
    if (layer.python_param.module):
        params['module'] = layer.python_param.module
    if (layer.python_param.layer):
        params['layer'] = layer.python_param.layer
    if (layer.python_param.param_str):
        params.update(eval(layer.python_param.param_str))
    if (layer.loss_weight):
        params['loss_weight'] = layer.loss_weight[0]
    ''' If its a loss layer ('1,0'), there will be no source endpoint, if
    its a data layer ('0,1') there will be no target endpoint, otherwise there
    will be both endpoints ('1,1')'''
    if (not layer.bottom):
        params['endPoint'] = '1, 0'
    elif ('loss' in layer.name.lower()):
        params['endPoint'] = '0, 1'
    else:
        params['endPoint'] = '1, 1'
    for param in params:
        if isinstance(params[param], list):
            params[param] = str(params[param])[1:-1]
    return params


layer_dict = {'Accuracy': Accuracy,
              'WindowData': WindowData,
              'Convolution': Convolution,
              'SoftmaxWithLoss': SoftmaxWithLoss,
              'InnerProduct': InnerProduct,
              'HDF5Data': HDF5Data,
              'Threshold': Threshold,
              'Deconvolution': Deconvolution,
              'Embed': Embed,
              'Log': Log,
              'Reduction': Reduction,
              'Slice': Slice,
              'Eltwise': Eltwise,
              'Dropout': Dropout,
              'PReLU': PReLU,
              'BatchNorm': BatchNorm,
              'MVN': MVN,
              'Recurrent': Recurrent,
              'Bias': Bias,
              'ContrastiveLoss': ContrastiveLoss,
              'Input': Input,
              'Exp': Exp,
              'ImageData': ImageData,
              'ReLU': ReLU,
              'MemoryData': MemoryData,
              'Crop': Crop,
              'SPP': SPP,
              'Pooling': Pooling,
              'Scale': Scale,
              'HingeLoss': HingeLoss,
              'Flatten': Flatten,
              'ArgMax': ArgMax,
              'BNLL': BNLL,
              'Data': Data,
              'HDF5Output': HDF5Output,
              'ELU': ELU,
              'DummyData': DummyData,
              'InfogainLoss': InfogainLoss,
              'TanH': TanH,
              'AbsVal': AbsVal,
              'Reshape': Reshape,
              'Power': Power,
              'Sigmoid': Sigmoid,
              'Python': Python,
              'LRN': LRN,
              'LSTM': Recurrent,
              'RNN': Recurrent
              }


@csrf_exempt
def import_prototxt(request):
    if request.method == 'POST':
        if ('file' in request.FILES) and \
           (request.FILES['file'].content_type == 'application/octet-stream'):
            try:
                prototxt = request.FILES['file']
            except Exception:
                return JsonResponse({'result': 'error',
                                     'error': 'No Prototxt model file found'})
        elif 'sample_id' in request.POST:
            try:
                prototxt = open(os.path.join(settings.BASE_DIR,
                                             'example', 'caffe',
                                             request.POST['sample_id'] + '.prototxt'), 'r')
            except Exception:
                return JsonResponse({'result': 'error',
                                     'error': 'No Prototxt model file found'})
        caffe_net = caffe_pb2.NetParameter()
        try:
            text_format.Merge(prototxt.read(), caffe_net)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid Prototxt'})

        net = {}
        i = 0
        blobMap = {}
        net_name = caffe_net.name
        hasTransformParam = ['ImageData', 'Data', 'WindowData']
        for layer in caffe_net.layer:
            id = "l" + str(i)
            input = []

            # this logic for phase has to be improved
            if len(layer.include):
                if (layer.include[0].HasField('phase')):
                    phase = layer.include[0].phase
                else:
                    phase = None
            else:
                phase = None

            params = {}
            if (layer.type in hasTransformParam):
                params['scale'] = layer.transform_param.scale
                params['mirror'] = layer.transform_param.mirror
                params['crop_size'] = layer.transform_param.crop_size
                if (layer.transform_param.mean_file != ''):
                    params['mean_file'] = layer.transform_param.mean_file
                elif (layer.transform_param.mean_value):
                    params['mean_value'] = str(
                        map(int, layer.transform_param.mean_value))[1:-1]
                params['force_color'] = layer.transform_param.force_color
                params['force_gray'] = layer.transform_param.force_gray

            if layer.type in layer_dict:
                layer_params = layer_dict[layer.type](layer)
                params.update(layer_params)

            jsonLayer = {
                'info': {
                    'type': layer.type,
                    'phase': phase
                },
                'connection': {
                    'input': [],
                    'output': []
                },
                'params': params
            }

            # this logic was written for a scenario where train and test layers are mixed up
            # But as we know, the only differences between the train and test phase are:
            # 1) input layer with different source in test
            # 2) some accuracy layers in test
            # If we consider these constraint, the below logic can be vastly reduced
            for bottom_blob in layer.bottom:
                if (bottom_blob != 'label'):
                    # if the current layer has a phase
                    # then only connect with layers of same phase
                    # if it has no phase then connect with all layers
                    if jsonLayer['info']['phase'] is not None:
                        phase = jsonLayer['info']['phase']
                        for bottomLayerId in blobMap[bottom_blob]:
                            if (net[bottomLayerId]['info']['phase'] == phase) or\
                                    (net[bottomLayerId]['info']['phase'] is None):
                                input.append(bottomLayerId)
                                net[bottomLayerId]['connection']['output'].append(
                                    id)
                    else:
                        for bottomLayerId in blobMap[bottom_blob]:
                            input.append(bottomLayerId)
                            net[bottomLayerId]['connection']['output'].append(
                                id)
            for top_blob in layer.top:
                if (top_blob != 'label'):
                    if top_blob in blobMap:
                        if top_blob in layer.bottom:
                            # check for in-place operations
                            # layer has no phase
                            # then remove all layer history
                            # and add this one to the top
                            # layer has phase then remove all layers with same phase and append this
                            if jsonLayer['info']['phase'] is not None:
                                phase = jsonLayer['info']['phase']
                                for layerId in blobMap[bottom_blob]:
                                    if net[layerId]['info']['phase'] == phase:
                                        blobMap[bottom_blob].remove(layerId)
                                blobMap[top_blob].append(id)
                            else:
                                blobMap[top_blob] = [id]
                        else:
                            blobMap[top_blob].append(id)
                    else:
                        blobMap[top_blob] = [id]
            jsonLayer['connection']['input'] = input
            net[id] = jsonLayer
            i = i + 1

        return JsonResponse({'result': 'success', 'net': net, 'net_name': net_name})
