from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
from caffe.proto import caffe_pb2
from google.protobuf import text_format


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

            # ********** Data Layers **********
            if (layer.type in hasTransformParam):
                params['scale'] = layer.transform_param.scale
                params['mirror'] = layer.transform_param.mirror
                params['crop_size'] = layer.transform_param.crop_size
                if (layer.transform_param.mean_file != ''):
                    params['mean_file'] = layer.transform_param.mean_file
                elif (layer.transform_param.mean_value):
                    params['mean_value'] = str(map(int, layer.transform_param.mean_value))[1:-1]
                params['force_color'] = layer.transform_param.force_color
                params['force_gray'] = layer.transform_param.force_gray

            if(layer.type == 'ImageData'):
                params['source'] = layer.image_data_param.source
                params['batch_size'] = layer.image_data_param.batch_size
                params['rand_skip'] = layer.image_data_param.rand_skip
                params['shuffle'] = layer.image_data_param.shuffle
                params['new_height'] = layer.image_data_param.new_height
                params['new_width'] = layer.image_data_param.new_width
                params['is_color'] = layer.image_data_param.is_color
                params['root_folder'] = layer.image_data_param.root_folder

            elif(layer.type == 'Data'):
                params['source'] = layer.data_param.source
                params['batch_size'] = layer.data_param.batch_size
                params['backend'] = layer.data_param.backend
                if (params['backend'] == 0):
                    params['backend'] = 'LEVELDB'
                else:
                    params['backend'] = 'LMDB'
                params['rand_skip'] = layer.data_param.rand_skip
                params['prefetch'] = layer.data_param.prefetch

            elif(layer.type == 'HDF5Data'):
                params['source'] = layer.hdf5_data_param.source
                params['batch_size'] = layer.hdf5_data_param.batch_size
                params['shuffle'] = layer.hdf5_data_param.shuffle

            elif(layer.type == 'HDF5Output'):
                params['file_name'] = layer.hdf5_output_param.file_name

            elif(layer.type == 'Input'):
                params['dim'] = str(map(int, layer.input_param.shape[0].dim))[1:-1]

            elif(layer.type == 'WindowData'):
                params['source'] = layer.window_data_param.source
                params['batch_size'] = layer.window_data_param.batch_size
                params['fg_threshold'] = layer.window_data_param.fg_threshold
                params['bg_threshold'] = layer.window_data_param.bg_threshold
                params['fg_fraction'] = layer.window_data_param.fg_fraction
                params['context_pad'] = layer.window_data_param.context_pad
                params['crop_mode'] = layer.window_data_param.crop_mode
                params['cache_images'] = layer.window_data_param.cache_images
                params['root_folder'] = layer.window_data_param.root_folder

            elif(layer.type == 'MemoryData'):
                params['batch_size'] = layer.memory_data_param.batch_size
                params['channels'] = layer.memory_data_param.channels
                params['height'] = layer.memory_data_param.height
                params['width'] = layer.memory_data_param.width

            elif(layer.type == 'DummyData'):
                params['dim'] = str(map(int, layer.dummy_data_param.shape[0].dim))[1:-1]
                params['type'] = str(layer.dummy_data_param.data_filler[0].type)

            # ********** Vision Layers **********
            elif(layer.type == 'Convolution'):
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

            elif(layer.type == 'Pooling'):
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

            elif(layer.type == 'SPP'):
                params['pool'] = layer.spp_param.pool
                params['pyramid_height'] = layer.spp_param.pyramid_height

            elif(layer.type == 'Crop'):
                if layer.crop_param.axis:
                    params['axis'] = layer.crop_param.axis
                if len(layer.crop_param.offset):
                    params['offset'] = layer.crop_param.offset[0]

            elif(layer.type == 'Deconvolution'):
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

            # ********** Recurrent Layers **********
            elif(layer.type == 'Recurrent' or layer.type == 'RNN' or
                 layer.type == 'LSTM'):
                params['num_output'] = layer.recurrent_param.num_output
                params['weight_filler'] = layer.recurrent_param.weight_filler.type
                params['bias_filler'] = layer.recurrent_param.bias_filler.type
                params['debug_info'] = layer.recurrent_param.debug_info
                params['expose_hidden'] = layer.recurrent_param.expose_hidden

            # ********** Common Layers **********
            elif(layer.type == 'InnerProduct'):
                params['num_output'] = layer.inner_product_param.num_output
                params['weight_filler'] = layer.inner_product_param.weight_filler.type
                params['bias_filler'] = layer.inner_product_param.bias_filler.type
                params['use_bias'] = layer.inner_product_param.bias_term

            elif(layer.type == 'Dropout'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'Embed'):
                params['bias_term'] = layer.embed_param.bias_term
                params['input_dim'] = layer.embed_param.input_dim
                params['num_output'] = layer.embed_param.num_output
                params['weight_filler'] = layer.embed_param.weight_filler.type
                params['bias_filler'] = layer.embed_param.bias_filler.type

            # ********** Normalisation Layers **********
            elif(layer.type == 'LRN'):
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

            elif(layer.type == 'MVN'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['normalize_variance'] = layer.mvn_param.normalize_variance
                params['across_channels'] = layer.mvn_param.across_channels
                params['eps'] = layer.mvn_param.eps

            elif(layer.type == 'BatchNorm'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['use_global_stats'] = layer.batch_norm_param.use_global_stats
                params['moving_average_fraction'] = layer.batch_norm_param.moving_average_fraction
                params['eps'] = layer.batch_norm_param.eps

            # ********** Activation/Neuron Layers **********
            elif(layer.type == 'ReLU'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['negative_slope'] = layer.relu_param.negative_slope

            elif(layer.type == 'PReLU'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['channel_shared'] = layer.prelu_param.channel_shared

            elif(layer.type == 'ELU'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['alpha'] = layer.elu_param.alpha

            elif(layer.type == 'Sigmoid'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'TanH'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'AbsVal'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'Power'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['power'] = layer.power_param.power
                params['scale'] = layer.power_param.scale
                params['shift'] = layer.power_param.shift

            elif(layer.type == 'Exp'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['base'] = layer.exp_param.base
                params['scale'] = layer.exp_param.scale
                params['shift'] = layer.exp_param.shift

            elif(layer.type == 'Log'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['base'] = layer.log_param.base
                params['scale'] = layer.log_param.scale
                params['shift'] = layer.log_param.shift

            elif(layer.type == 'BNLL'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'Threshold'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True
                params['threshold'] = layer.threshold_param.threshold

            elif(layer.type == 'Bias'):
                params['axis'] = layer.bias_param.axis
                params['num_axes'] = layer.bias_param.num_axes
                params['filler'] = layer.bias_param.filler.type

            elif(layer.type == 'Scale'):
                params['axis'] = layer.scale_param.axis
                params['num_axes'] = layer.scale_param.num_axes
                params['filler'] = layer.scale_param.filler.type
                params['bias_term'] = layer.scale_param.bias_term
                params['bias_filler'] = layer.scale_param.bias_filler.type

            # ********** Utility Layers **********
            elif(layer.type == 'Flatten'):
                params['axis'] = layer.flatten_param.axis
                params['end_axis'] = layer.flatten_param.end_axis

            elif(layer.type == 'Reshape'):
                params['dim'] = str(map(int, layer.reshape_param.shape.dim))[1:-1]

            elif(layer.type == 'Slice'):
                params['slice_point'] = str(map(int, layer.slice_param.slice_point))[1:-1]
                params['axis'] = layer.slice_param.axis
                params['slice_dim'] = layer.slice_param.slice_dim

            elif(layer.type == 'Eltwise'):
                opMap = {
                    0: 'Product',
                    1: 'Sum',
                    2: 'Maximum'
                }
                if layer.eltwise_param.operation:
                    params['layer_type'] = opMap[layer.eltwise_param.operation]
                else:
                    params['layer_type'] = 'Sum'

            # This layer is currently not supported as there is no bottom blob
            # elif(layer.type == 'Parameter'):
            #    params['shape'] = str(map(int, layer.parameter_param.shape.dim))[1:-1]

            elif(layer.type == 'Reduction'):
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

            elif(layer.type == 'ArgMax'):
                params['out_max_val'] = layer.argmax_param.out_max_val
                params['top_k'] = layer.argmax_param.top_k
                params['axis'] = layer.argmax_param.axis

            # ********** Loss Layers **********
            elif(layer.type == 'InfogainLoss'):
                params['source'] = layer.infogain_loss_param.source
                params['axis'] = layer.infogain_loss_param.axis

            elif(layer.type == 'SoftmaxWithLoss'):
                params['axis'] = layer.softmax_param.axis

            elif(layer.type == 'HingeLoss'):
                params['norm'] = layer.hinge_loss_param.norm

            elif(layer.type == 'Accuracy'):
                params['top_k'] = layer.accuracy_param.top_k
                params['axis'] = layer.accuracy_param.axis

            elif(layer.type == 'ContrastiveLoss'):
                params['margin'] = layer.contrastive_loss_param.margin
                params['legacy_version'] = layer.contrastive_loss_param.legacy_version

            # ********** Python Layer **********
            elif(layer.type == 'Python'):
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

            # this logic was written for a scenerio where train and test layers are mixed up
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
                                net[bottomLayerId]['connection']['output'].append(id)
                    else:
                        for bottomLayerId in blobMap[bottom_blob]:
                            input.append(bottomLayerId)
                            net[bottomLayerId]['connection']['output'].append(id)
            for top_blob in layer.top:
                if (top_blob != 'label'):
                    if top_blob in blobMap:
                        if top_blob in layer.bottom:
                            # check for inplace operations
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
