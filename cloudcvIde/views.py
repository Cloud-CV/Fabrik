from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import yaml
from django.http import HttpResponse
import caffe
from caffe import layers as L
from caffe.proto import caffe_pb2
from google.protobuf import text_format
import re


def index(request):
    return render(request, 'cloudcvIde/index.html')


@csrf_exempt
def export(request):
    if request.method == 'POST':

        net = yaml.safe_load(request.POST.get('net'))

        # assumption: a layer can accept only one input blob
        # the data layer produces two blobs: data and label
        # the loss layer requires two blobs: <someData> and label
        # the label blob is hardcoded.
        # layers name have to be unique

        # custom DFS of the network
        stack = []
        layersProcessed = {}
        processOrder = []
        blobNames = {}
        for layerId in net:
            layersProcessed[layerId] = False
            inplace = False
            if 'inplace' in net[layerId]['params']:
                # check this new checkbox at front
                if net[layerId]['params']['inplace']['value'] is True:
                    inplace = True
            blobNames[layerId] = {
                'bottom': None,
                'top': None,
                'inplace': inplace
            }
        blobId = 0

        def isProcessPossible(layerId):
            inputs = net[layerId]['connection']['input']
            for layerId in inputs:
                if layersProcessed[layerId] is False:
                    return False
            return True

        # finding the data layer
        for layerId in net:
            if(net[layerId]['info']['type'] == 'Data'):
                stack.append(layerId)

        def changeTopBlobName(layerId, newName):
            if blobNames[layerId]['top'] == newName:
                return
            else:
                blobNames[layerId]['top'] = newName
                if blobNames[layerId]['inplace']:
                    blobNames[layerId]['bottom'] = newName
                    for i1 in net[layerId]['connection']['input']:
                        changeTopBlobName(i1, newName)

        while len(stack):

            i = len(stack) - 1

            while isProcessPossible(stack[i]) is False:
                i = i - 1

            layerId = stack[i]
            stack.remove(stack[i])

            inputs = net[layerId]['connection']['input']
            if len(inputs) > 0:
                topBlobNameOfInputs = blobNames[inputs[0]]['top']
                for i1 in inputs:
                    if blobNames[i1]['top'] != topBlobNameOfInputs:
                        changeTopBlobName(i1, topBlobNameOfInputs)
                blobNames[layerId]['bottom'] = topBlobNameOfInputs

            if blobNames[layerId]['inplace']:
                blobNames[layerId]['top'] = blobNames[layerId]['bottom']
            else:
                blobNames[layerId]['top'] = "blob"+str(blobId)
                blobId = blobId + 1

            for i1 in net[layerId]['connection']['output']:
                if i1 not in stack:
                    stack.append(i1)

            layersProcessed[layerId] = True
            processOrder.append(layerId)

        # *****************************
        # we have figured out the final blob names
        # but now there is a problem with inplace operations with pycaffe
        # it requires different blob names
        # now we have to again tweak blob names
        # so that pycaffe again corrects them

        # making all common layers to have seperate bottom blobs
        # for train and test phases
        for layerId in net:
            layerPhase = net[layerId]['info']['phase']
            if layerPhase is None:
                blobNames[layerId]['0'] = blobNames[layerId]['bottom']
                blobNames[layerId]['1'] = blobNames[layerId]['bottom']

        # changing blob names for all layers attached to a layer
        # with inplace operation
        # (taking into account the phase)
        for layerId in blobNames:
            if blobNames[layerId]['inplace'] is True:
                layerPhase = net[layerId]['info']['phase']
                outputs = net[layerId]['connection']['output']
                for i1 in outputs:
                    p = net[i1]['info']['phase']
                    if p is None:
                        blobNames[i1][layerPhase] = 'blob' + str(blobId)
                    else:
                        blobNames[i1]['bottom'] = 'blob' + str(blobId)
                blobNames[layerId]['top'] = 'blob' + str(blobId)
                blobId = blobId + 1

        # ******************************

        ns = caffe.NetSpec()
        ns_test = caffe.NetSpec()

        for layerId in processOrder:

            layer = net[layerId]
            layerParams = layer['params']
            layerType = layer['info']['type']
            layerPhase = layer['info']['phase']
            topBlob = blobNames[layerId]['top']

            if (layerType == 'Data'):
                source = layerParams['source']['value']
                batch_size = int(
                    float(layerParams['batch_size']['value']))
                scale = float(layerParams['scale']['value'])
                backend = layerParams['backend']['value']
                if(backend == 'LEVELDB'):
                    backend = 0
                elif(backend == 'LMDB'):
                    backend = 1

                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob], ns.label = L.Data(
                            ntop=2,
                            transform_param={
                                'scale': scale
                            },
                            data_param={
                                'source': source,
                                'batch_size': batch_size,
                                'backend': backend
                            },
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob], ns_test.label = L.Data(
                            ntop=2,
                            transform_param={
                                'scale': scale
                            },
                            data_param={
                                'source': source,
                                'batch_size': batch_size,
                                'backend': backend
                            },
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob], ns.label = L.Data(
                        ntop=2,
                        transform_param={
                            'scale': scale
                        },
                        data_param={
                            'source': source,
                            'batch_size': batch_size,
                            'backend': backend
                        })
                    ns_test[topBlob], ns_test.label = L.Data(
                        ntop=2,
                        transform_param={
                            'scale': scale
                        },
                        data_param={
                            'source': source,
                            'batch_size': batch_size,
                            'backend': backend
                        })

            elif (layerType == 'Convolution'):
                num_output = int(float(layerParams['num_output']['value']))
                # pad = int(float(layerParams['pad']['value']))
                pad = 0
                kernel_size = int(float(layerParams['kernel_size']['value']))
                stride = int(float(layerParams['stride']['value']))
                weight_filler = layerParams['weight_filler']['value']
                bias_filler = layerParams['bias_filler']['value']

                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.Convolution(
                            ns[blobNames[layerId]['bottom']],
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
                            ],
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.Convolution(
                            ns_test[blobNames[layerId]['bottom']],
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
                            ],
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.Convolution(
                        ns[blobNames[layerId]['0']],
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
                    ns_test[topBlob] = L.Convolution(
                        ns_test[blobNames[layerId]['1']],
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

            elif (layerType == 'ReLU'):
                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.ReLU(
                            ns[blobNames[layerId]['bottom']],
                            in_place=True,
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.ReLU(
                            ns_test[blobNames[layerId]['bottom']],
                            in_place=True,
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.ReLU(
                        ns[blobNames[layerId]['0']],
                        in_place=True)
                    ns_test[topBlob] = L.ReLU(
                        ns_test[blobNames[layerId]['1']],
                        in_place=True)

            elif (layerType == 'Pooling'):
                # pad = int(float(layerParams['pad']['value']))
                pad = 0
                kernel_size = int(float(layerParams['kernel_size']['value']))
                stride = int(float(layerParams['stride']['value']))
                pool = layerParams['pool']['value']
                if(pool == 'MAX'):
                    pool = 0
                elif(pool == 'AVE'):
                    pool = 1
                elif(pool == 'STOCHASTIC'):
                    pool = 2

                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.Pooling(
                            ns[blobNames[layerId]['bottom']],
                            pooling_param={
                                'pad': pad,
                                'kernel_size': kernel_size,
                                'stride': stride,
                                'pool': pool
                            },
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.Pooling(
                            ns_test[blobNames[layerId]['bottom']],
                            pooling_param={
                                'pad': pad,
                                'kernel_size': kernel_size,
                                'stride': stride,
                                'pool': pool
                            },
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.Pooling(
                        ns[blobNames[layerId]['0']],
                        pooling_param={
                            'pad': pad,
                            'kernel_size': kernel_size,
                            'stride': stride,
                            'pool': pool
                        })
                    ns_test[topBlob] = L.Pooling(
                        ns_test[blobNames[layerId]['1']],
                        pooling_param={
                            'pad': pad,
                            'kernel_size': kernel_size,
                            'stride': stride,
                            'pool': pool
                        })

            elif (layerType == 'InnerProduct'):
                num_output = int(float(layerParams['num_output']['value']))
                weight_filler = layerParams['weight_filler']['value']
                bias_filler = layerParams['bias_filler']['value']

                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.InnerProduct(
                            ns[blobNames[layerId]['bottom']],
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
                            ],
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.InnerProduct(
                            ns_test[blobNames[layerId]['bottom']],
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
                            ],
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.InnerProduct(
                        ns[blobNames[layerId]['0']],
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
                    ns_test[topBlob] = L.InnerProduct(
                        ns_test[blobNames[layerId]['1']],
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

            elif (layerType == 'SoftmaxWithLoss'):
                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.SoftmaxWithLoss(
                            ns[blobNames[layerId]['bottom']],
                            ns.label,
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.SoftmaxWithLoss(
                            ns_test[blobNames[layerId]['bottom']],
                            ns_test.label,
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.SoftmaxWithLoss(
                        ns[blobNames[layerId]['0']],
                        ns.label)
                    ns_test[topBlob] = L.SoftmaxWithLoss(
                        ns_test[blobNames[layerId]['1']],
                        ns_test.label)

            elif (layerType == 'Accuracy'):
                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.Accuracy(
                            ns[blobNames[layerId]['bottom']],
                            ns.label,
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.Accuracy(
                            ns_test[blobNames[layerId]['bottom']],
                            ns_test.label,
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.Accuracy(
                        ns[blobNames[layerId]['0']],
                        ns.label)
                    ns_test[topBlob] = L.Accuracy(
                        ns_test[blobNames[layerId]['1']],
                        ns_test.label)

        train = str(ns.to_proto())
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

        return HttpResponse(
            json.dumps({'result': prototxt}),
            content_type="application/json")


@csrf_exempt
def importModel(request):
    if request.method == 'POST':
        prototxt = request.FILES['file']

        caffe_net = caffe_pb2.NetParameter()
        text_format.Merge(prototxt.read(), caffe_net)

        d = {}
        i = 0
        b = {}
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
                params['scale'] = layer.data_param.scale

            elif(layer.type == 'Convolution'):
                if len(layer.convolution_param.kernel_size):
                    params['kernel_size'] = layer.convolution_param.kernel_size[0]
                if len(layer.convolution_param.pad):
                    params['pad'] = layer.convolution_param.pad[0]
                if len(layer.convolution_param.stride):
                    params['stride'] = layer.convolution_param.stride[0]
                params['weight_filler'] = layer.convolution_param.weight_filler.type
                params['bias_filler'] = layer.convolution_param.bias_filler.type
                params['num_output'] = layer.convolution_param.num_output

            elif(layer.type == 'ReLU'):
                if(layer.top == layer.bottom):
                    params['inplace'] = True

            elif(layer.type == 'Pooling'):
                params['pad'] = layer.pooling_param.pad
                params['stride'] = layer.pooling_param.stride
                params['kernel_size'] = layer.pooling_param.kernel_size
                params['pool'] = layer.pooling_param.pool

            elif(layer.type == 'InnerProduct'):
                params['num_output'] = layer.inner_product_param.num_output
                params['weight_filler'] = layer.inner_product_param.weight_filler.type
                params['bias_filler'] = layer.inner_product_param.bias_filler.type

            elif(layer.type == 'SoftmaxWithLoss'):
                pass
            elif(layer.type == 'Accuracy'):
                pass

            l = {
                'info': {
                    'type': layer.type,
                    'phase': phase
                },
                'connection': {
                    'input': [],
                    'output': []
                },
                'importedParams': params
            }
            for bottom_blob in layer.bottom:
                if (bottom_blob != 'label'):
                    # if the current layer has a phase
                    # then only connect with layers of same phase
                    # if it has no phase then connect with all layers
                    if l['info']['phase'] is not None:
                        p = l['info']['phase']
                        for bottomLayerId in b[bottom_blob]:
                            if (d[bottomLayerId]['info']['phase'] == p) or (d[bottomLayerId]['info']['phase'] is None):
                                input.append(bottomLayerId)
                                d[bottomLayerId]['connection']['output'].append(id)
                    else:
                        for bottomLayerId in b[bottom_blob]:
                            input.append(bottomLayerId)
                            d[bottomLayerId]['connection']['output'].append(id)
            for top_blob in layer.top:
                if (top_blob != 'label'):
                    if top_blob in b:
                        if top_blob in layer.bottom:
                            # check for inplace operations
                            # layer has no phase
                            # then remove all layer history
                            # and add this one to the top
                            # layer has phase then remove all layers with same phase and append this
                            if l['info']['phase'] is not None:
                                p = l['info']['phase']
                                for i1 in b[bottom_blob]:
                                    if d[i1]['info']['phase'] == p:
                                        b[bottom_blob].remove(i1)
                                b[top_blob].append(id)
                            else:
                                b[top_blob] = [id]
                        else:
                            b[top_blob].append(id)
                    else:
                        b[top_blob] = [id]
            l['connection']['input'] = input
            d[id] = l
            i = i + 1

        return HttpResponse(
            json.dumps({'result': 'success', 'net': d}),
            content_type="application/json")
