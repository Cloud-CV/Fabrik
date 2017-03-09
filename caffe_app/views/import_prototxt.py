from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import yaml
from caffe.proto import caffe_pb2
from google.protobuf import text_format

@csrf_exempt
def importPrototxt(request):
    if request.method == 'POST':
        try:
            prototxt = request.FILES['file']
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'No Prototxt model file found'})

        caffe_net = caffe_pb2.NetParameter()

        try:
            text_format.Merge(prototxt.read(), caffe_net)
        except Exception:
            return JsonResponse({'result': 'error', 'error': 'Invalid Prototxt'})


        net = {}
        i = 0
        blobMap = {}
        net_name = caffe_net.name
        for layer in caffe_net.layer:
            id = "l" + str(i)
            input = []

            # this logic for phase has to be improved
            if len(layer.include):
                phase = layer.include[0].phase
            else:
                phase = None

            params = {}
            if(layer.type == 'Data'):
                params['source'] = layer.data_param.source
                params['batch_size'] = layer.data_param.batch_size
                params['backend'] = layer.data_param.backend
                params['scale'] = layer.transform_param.scale

            elif(layer.type == 'Crop'):
                if layer.crop_param.axis:
                    params['axis'] = layer.crop_param.axis
                if len(layer.crop_param.offset):
                    params['offset'] = layer.crop_param.offset[0]

            elif(layer.type == 'Convolution'):
                if len(layer.convolution_param.kernel_size):
                    params['kernel_h'] = layer.convolution_param.kernel_h or layer.convolution_param.kernel_size[0]
                    params['kernel_w'] = layer.convolution_param.kernel_w or layer.convolution_param.kernel_size[0]
                if len(layer.convolution_param.pad):
                    params['pad_h'] = layer.convolution_param.pad_h or layer.convolution_param.pad[0]
                    params['pad_w'] = layer.convolution_param.pad_w or layer.convolution_param.pad[0]
                if len(layer.convolution_param.stride):
                    params['stride_h'] = layer.convolution_param.stride_h or layer.convolution_param.stride[0]
                    params['stride_w'] = layer.convolution_param.stride_w or layer.convolution_param.stride[0]
                params['weight_filler'] = layer.convolution_param.weight_filler.type
                params['bias_filler'] = layer.convolution_param.bias_filler.type
                params['num_output'] = layer.convolution_param.num_output

            elif(layer.type == 'Deconvolution'):
                if len(layer.convolution_param.kernel_size):
                    params['kernel_h'] = layer.convolution_param.kernel_h or layer.convolution_param.kernel_size[0]
                    params['kernel_w'] = layer.convolution_param.kernel_w or layer.convolution_param.kernel_size[0]
                if len(layer.convolution_param.pad):
                    params['pad_h'] = layer.convolution_param.pad_h or layer.convolution_param.pad[0]
                    params['pad_w'] = layer.convolution_param.pad_w or layer.convolution_param.pad[0]
                if len(layer.convolution_param.stride):
                    params['stride_h'] = layer.convolution_param.stride_h or layer.convolution_param.stride[0]
                    params['stride_w'] = layer.convolution_param.stride_w or layer.convolution_param.stride[0]
                params['weight_filler'] = layer.convolution_param.weight_filler.type
                params['bias_filler'] = layer.convolution_param.bias_filler.type
                params['num_output'] = layer.convolution_param.num_output

            elif(layer.type == 'ReLU'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'Eltwise'):
                if layer.eltwise_param.operation:
                    params['operation'] = layer.eltwise_param.operation
                else:
                    params['operation'] = 1

            elif(layer.type == 'Pooling'):
                params['pad_h'] = layer.pooling_param.pad_h or layer.pooling_param.pad
                params['pad_w'] = layer.pooling_param.pad_w or layer.pooling_param.pad
                params['stride_h'] = layer.pooling_param.stride_h or layer.pooling_param.stride
                params['stride_w'] = layer.pooling_param.stride_w or layer.pooling_param.stride
                params['kernel_h'] = layer.pooling_param.kernel_h or layer.pooling_param.kernel_size
                params['kernel_w'] = layer.pooling_param.kernel_w or layer.pooling_param.kernel_size
                params['pool'] = layer.pooling_param.pool

            elif(layer.type == 'InnerProduct'):
                params['num_output'] = layer.inner_product_param.num_output
                params['weight_filler'] = layer.inner_product_param.weight_filler.type
                params['bias_filler'] = layer.inner_product_param.bias_filler.type

            elif(layer.type == 'SoftmaxWithLoss'):
                pass
            elif(layer.type == 'Accuracy'):
                pass
            elif(layer.type == 'Input'):
                params['dim'] = str(map(int,layer.input_param.shape[0].dim))[1:-1]
                # string '64,1,28,28'
            elif(layer.type == 'LSTM'):
                params['num_output'] = layer.recurrent_param.num_output
                params['weight_filler'] = layer.recurrent_param.weight_filler.type
                params['bias_filler'] = layer.recurrent_param.bias_filler.type
            
            elif(layer.type == 'Embed'):
                params['bias_term'] = layer.embed_param.bias_term
                params['input_dim'] = layer.embed_param.input_dim
                params['num_output'] = layer.embed_param.num_output
                params['weight_filler'] = layer.embed_param.weight_filler.type
            
            elif(layer.type == 'Reshape'):
                params['dim'] = str(map(int,layer.reshape_param.shape.dim))[1:-1]
            
            elif(layer.type == 'HDF5Data'):
                params['source'] = layer.hdf5_data_param.source
                params['batch_size'] = layer.hdf5_data_param.batch_size
            elif(layer.type == 'BatchNorm'):
                params['use_global_stats'] = layer.batch_norm_param.use_global_stats
            elif(layer.type == 'Scale'):
                params['bias_term'] = layer.scale_param.bias_term
            elif(layer.type == 'Eltwise'):
                params['operation'] = layer.eltwise_param.operation

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

            # this logic was written for a general scenerio(where train and test layers are mixed up)
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
                            if (net[bottomLayerId]['info']['phase'] == phase) or (net[bottomLayerId]['info']['phase'] is None):
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

        return JsonResponse({'result': 'success', 'net': net, 'net_name':net_name })
