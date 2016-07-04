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
from datetime import datetime
import random, string
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


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
                if net[layerId]['params']['inplace'] is True:
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
                    for inputId in net[layerId]['connection']['input']:
                        changeTopBlobName(inputId, newName)

        while len(stack):

            i = len(stack) - 1

            while isProcessPossible(stack[i]) is False:
                i = i - 1

            layerId = stack[i]
            stack.remove(stack[i])

            inputs = net[layerId]['connection']['input']
            if len(inputs) > 0:
                topBlobNameOfInputs = blobNames[inputs[0]]['top']
                for inputId in inputs:
                    if blobNames[inputId]['top'] != topBlobNameOfInputs:
                        changeTopBlobName(inputId, topBlobNameOfInputs)
                blobNames[layerId]['bottom'] = topBlobNameOfInputs

            if blobNames[layerId]['inplace']:
                blobNames[layerId]['top'] = blobNames[layerId]['bottom']
            else:
                blobNames[layerId]['top'] = "blob"+str(blobId)
                blobId = blobId + 1

            for outputId in net[layerId]['connection']['output']:
                if outputId not in stack:
                    stack.append(outputId)

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
                for outputId in outputs:
                    phase = net[outputId]['info']['phase']
                    if phase is None:
                        blobNames[outputId][layerPhase] = 'blob' + str(blobId)
                    else:
                        blobNames[outputId]['bottom'] = 'blob' + str(blobId)
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

                data_param = {}
                if layerParams['source'] != '':
                    data_param['source'] = layerParams['source']
                    # hardcoding mnsit dataset -change this later
                    if layerPhase is not None:
                        if int(layerPhase) == 0:
                            data_param['source'] = BASE_DIR+'/cloudcvIde/media/dataset/mnsit/mnist_train_lmdb'
                        elif int(layerPhase) == 1:
                            data_param['source'] = BASE_DIR+'/cloudcvIde/media/dataset/mnsit/mnist_test_lmdb'
                if layerParams['batch_size'] != '':
                    data_param['batch_size'] = int(float(layerParams['batch_size']))
                if layerParams['backend'] != '':
                    backend = layerParams['backend']
                    if(backend == 'LEVELDB'):
                        backend = 0
                    elif(backend == 'LMDB'):
                        backend = 1
                    data_param['backend'] = backend

                transform_param = {}
                if layerParams['scale'] != '':
                    transform_param['scale'] = float(layerParams['scale'])


                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob], ns.label = L.Data(
                            ntop=2,
                            transform_param=transform_param,
                            data_param=data_param,
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob], ns_test.label = L.Data(
                            ntop=2,
                            transform_param=transform_param,
                            data_param=data_param,
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob], ns.label = L.Data(
                        ntop=2,
                        transform_param=transform_param,
                        data_param=data_param)
                    ns_test[topBlob], ns_test.label = L.Data(
                        ntop=2,
                        transform_param=transform_param,
                        data_param=data_param)

            elif (layerType == 'Convolution'):

                convolution_param={}
                if layerParams['kernel_size'] != '':
                    convolution_param['kernel_size'] = int(float(layerParams['kernel_size']))
                if layerParams['stride'] != '':
                    convolution_param['stride'] = int(float(layerParams['stride']))
                if layerParams['num_output'] != '':
                    convolution_param['num_output'] = int(float(layerParams['num_output']))
                if layerParams['pad'] != '':
                    convolution_param['pad'] = int(float(layerParams['pad']))
                if layerParams['weight_filler'] != '':
                    convolution_param['weight_filler']={}
                    convolution_param['weight_filler']['type'] = layerParams['weight_filler']
                if layerParams['bias_filler'] != '':
                    convolution_param['bias_filler']={}
                    convolution_param['bias_filler']['type'] = layerParams['bias_filler']

                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.Convolution(
                            ns[blobNames[layerId]['bottom']],
                            convolution_param=convolution_param,
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
                            convolution_param=convolution_param,
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
                        convolution_param=convolution_param,
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
                        convolution_param=convolution_param,
                        param=[
                            {
                                'lr_mult': 1
                            },
                            {
                                'lr_mult': 2
                            }
                        ])

            elif (layerType == 'ReLU'):
                inplace = layerParams['inplace']
                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.ReLU(
                            ns[blobNames[layerId]['bottom']],
                            in_place=inplace,
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.ReLU(
                            ns_test[blobNames[layerId]['bottom']],
                            in_place=inplace,
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.ReLU(
                        ns[blobNames[layerId]['0']],
                        in_place=inplace)
                    ns_test[topBlob] = L.ReLU(
                        ns_test[blobNames[layerId]['1']],
                        in_place=inplace)

            elif (layerType == 'Pooling'):

                pooling_param={}
                if layerParams['kernel_size'] != '':
                    pooling_param['kernel_size'] = int(float(layerParams['kernel_size']))
                if layerParams['stride'] != '':
                    pooling_param['stride'] = int(float(layerParams['stride']))
                if layerParams['pad'] != '':
                    pooling_param['pad'] = int(float(layerParams['pad']))
                if layerParams['pool'] != '':
                    pool = layerParams['pool']
                    if(pool == 'MAX'):
                        pool = 0
                    elif(pool == 'AVE'):
                        pool = 1
                    elif(pool == 'STOCHASTIC'):
                        pool = 2
                    pooling_param['pool'] = pool


                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.Pooling(
                            ns[blobNames[layerId]['bottom']],
                            pooling_param=pooling_param,
                            include={
                                'phase': 0
                            })
                    elif int(layerPhase) == 1:
                        ns_test[topBlob] = L.Pooling(
                            ns_test[blobNames[layerId]['bottom']],
                            pooling_param=pooling_param,
                            include={
                                'phase': 1
                            })
                else:
                    ns[topBlob] = L.Pooling(
                        ns[blobNames[layerId]['0']],
                        pooling_param=pooling_param)
                    ns_test[topBlob] = L.Pooling(
                        ns_test[blobNames[layerId]['1']],
                        pooling_param=pooling_param)

            elif (layerType == 'InnerProduct'):

                inner_product_param={}
                if layerParams['num_output'] != '':
                    inner_product_param['num_output'] = int(float(layerParams['num_output']))
                if layerParams['weight_filler'] != '':
                    inner_product_param['weight_filler']={}
                    inner_product_param['weight_filler']['type'] = layerParams['weight_filler']
                if layerParams['bias_filler'] != '':
                    inner_product_param['bias_filler']={}
                    inner_product_param['bias_filler']['type'] = layerParams['bias_filler']

                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        ns[topBlob] = L.InnerProduct(
                            ns[blobNames[layerId]['bottom']],
                            inner_product_param=inner_product_param,
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
                            inner_product_param=inner_product_param,
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
                        inner_product_param=inner_product_param,
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
                        inner_product_param=inner_product_param,
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

        randomId=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)

        with open(BASE_DIR+'/cloudcvIde/media/prototxt/'+randomId+'.prototxt', 'w') as f:
            f.write(prototxt)

        return HttpResponse(
            json.dumps({'result': prototxt, 'id': randomId}),
            content_type="application/json")


@csrf_exempt
def importModel(request):
    if request.method == 'POST':
        prototxt = request.FILES['file']

        caffe_net = caffe_pb2.NetParameter()
        text_format.Merge(prototxt.read(), caffe_net)

        net = {}
        i = 0
        blobMap = {}
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

        return HttpResponse(
            json.dumps({'result': 'success', 'net': net}),
            content_type="application/json")
