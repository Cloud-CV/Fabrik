from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import yaml
from django.http import HttpResponse
import caffe
from caffe import layers as L


def index(request):
    return render(request, 'cloudcvIde/index.html')


@csrf_exempt
def export(request):
    if request.method == 'POST':

        net = yaml.safe_load(request.POST.get('net'))

        # assumption: we have a linear net.
        # the data layer produces two blobs: data and label
        # the loss layer requires two blobs: <someData> and label
        # the label blob is hardcoded.
        # layers name have to be unique

        # first we find the data layer and then follow output
        # connection till we reach loss layer

        # finding the data layer
        for layerId in net:
            if(net[layerId]['info']['type'] == 'input'):
                break

        ns = caffe.NetSpec()
        ns_test = caffe.NetSpec()
        prevLayerName = None

        while layerId is not None:
            layer = net[layerId]
            layerName = layer['props']['name']['value']
            layerParams = layer['params']
            layerType = layer['info']['type']

            if (layerType == 'input'):
                train_source = layerParams['train_source']['value']
                test_source = layerParams['test_source']['value']
                train_batch_size = int(
                    float(layerParams['train_batch_size']['value']))
                test_batch_size = int(
                    float(layerParams['test_batch_size']['value']))
                scale = float(layerParams['scale']['value'])
                backend = layerParams['backend']['value']
                if(backend == 'LEVELDB'):
                    backend = 0
                elif(backend == 'LMDB'):
                    backend = 1
                # TRAIN phase data layer
                ns[layerName], ns.label = L.Data(
                    ntop=2,
                    transform_param={
                        'scale': scale
                    },
                    data_param={
                        'source': train_source,
                        'batch_size': train_batch_size,
                        'backend': backend
                    },
                    include={
                        'phase': caffe.TRAIN
                    })
                # TEST phase data layer
                ns_test[layerName], ns_test.label = L.Data(
                    ntop=2,
                    transform_param={
                        'scale': scale
                    },
                    data_param={
                        'source': test_source,
                        'batch_size': test_batch_size,
                        'backend': backend
                    },
                    include={
                        'phase': caffe.TEST
                    })

            elif (layerType == 'conv'):
                num_output = int(float(layerParams['num_output']['value']))
                pad = int(float(layerParams['pad']['value']))
                kernel_size = int(float(layerParams['kernel_size']['value']))
                stride = int(float(layerParams['stride']['value']))
                weight_filler = layerParams['weight_filler']['value']
                bias_filler = layerParams['bias_filler']['value']
                ns[layerName] = L.Convolution(
                    ns[prevLayerName],
                    convolution_param={
                        'kernel_size': kernel_size,
                        'stride': stride,
                        'num_output': num_output,
                        'pad': pad,
                        'weight_filler': {
                            'type': weight_filler
                        },
                        'bias_filler': {
                            'type': bias_filler
                        }
                    },
                    param=[
                        {
                            'lr_mult': 1
                        },
                        {
                            'lr_mult': 2
                        }
                    ])

            elif (layerType == 'relu'):
                ns[layerName] = L.ReLU(ns[prevLayerName], in_place=True)

            elif (layerType == 'pool'):
                pad = int(float(layerParams['pad']['value']))
                kernel_size = int(float(layerParams['kernel_size']['value']))
                stride = int(float(layerParams['stride']['value']))
                pool = layerParams['pool']['value']
                if(pool == 'MAX'):
                    pool = 0
                elif(pool == 'AVE'):
                    pool = 1
                elif(pool == 'STOCHASTIC'):
                    pool = 2
                ns[layerName] = L.Pooling(
                    ns[prevLayerName],
                    pooling_param={
                        'pad': pad,
                        'kernel_size': kernel_size,
                        'stride': stride,
                        'pool': pool
                    })

            elif (layerType == 'fc'):
                num_output = int(float(layerParams['num_output']['value']))
                weight_filler = layerParams['weight_filler']['value']
                bias_filler = layerParams['bias_filler']['value']
                ns[layerName] = L.InnerProduct(
                    ns[prevLayerName],
                    inner_product_param={
                        'num_output': num_output,
                        'weight_filler': {
                            'type': weight_filler
                        },
                        'bias_filler': {
                            'type': bias_filler
                        }
                    },
                    param=[
                        {
                            'lr_mult': 1
                        },
                        {
                            'lr_mult': 2
                        }
                    ])

            elif (layerType == 'loss'):
                ns[layerName] = L.SoftmaxWithLoss(
                    ns[prevLayerName],
                    ns.label)

            prevLayerName = layerName
            layerId = layer['connection']['output']

        prototxt = str(ns_test.to_proto()) + str(ns.to_proto())

        return HttpResponse(
            json.dumps({'result': prototxt}),
            content_type="application/json")
