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
import collections
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def get_iterable(x):
    if isinstance(x, collections.Iterable):
        return x
    else:
        return (x,)

def index(request):
    return render(request, 'cloudcvIde/index.html')

def convertNetToPrototxt(net):
    # assumption: a layer can accept only one input blob
    # the data layer produces two blobs: data and label
    # the loss layer requires two blobs: <someData> and label
    # the label blob is hardcoded.
    # layers name have to be unique

    # custom DFS of the network
    print net

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
    for layerId in net:
        if(net[layerId]['info']['type'] == 'Data' or net[layerId]['info']['type'] == 'Input'):
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
            if len(inputs) == 2 and (net[inputs[0]]['info']['phase'] is not None) and (net[inputs[1]]['info']['phase']):
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
        topBlob = blobNames[layerId]['top']

        if (layerType == 'Data' or layerType == 'Input'):

            # This is temporary
            # Has to be improved later
            # If we have data layer then it is converted to input layer with some default dimensions
            '''
            data_param = {}
            if layerParams['source'] != '':
                data_param['source'] = layerParams['source']
                # hardcoding mnsit dataset -change this later
                if layerPhase is not None:
                    if int(layerPhase) == 0:
                        data_param['source'] = 'examples/mnist/mnist_train_lmdb'
                    elif int(layerPhase) == 1:
                        data_param['source'] = 'examples/mnist/mnist_test_lmdb'
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
                caffeLayer = get_iterable(L.Data(
                    ntop=1,
                    transform_param=transform_param,
                    data_param=data_param,
                    include={
                        'phase': int(layerPhase)
                    }))
                if int(layerPhase) == 0:
                    #for key, value in zip(blobNames[layerId]['top'] + ['label'], caffeLayer):
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns_train[key] = value
                elif int(layerPhase) == 1:
                    #for key, value in zip(blobNames[layerId]['top'] + ['label'], caffeLayer):
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns_test[key] = value
            else:
                for ns in (ns_train,ns_test):
                    caffeLayer = get_iterable(L.Data(
                        ntop=2,
                        transform_param=transform_param,
                        data_param=data_param))
                    #for key, value in zip(blobNames[layerId]['top'] + ['label'], caffeLayer):
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns[key] = value
            '''

            if 'dim' not in layerParams:
                layerParams['dim'] = '10,3,224,224'

            if layerPhase is not None:
                caffeLayer = get_iterable(L.Input(
                    input_param={'shape':{'dim':map(int,layerParams['dim'].split(','))}},
                    include={
                        'phase': int(layerPhase)
                    }))
                if int(layerPhase) == 0:
                    #for key, value in zip(blobNames[layerId]['top'] + ['label'], caffeLayer):
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns_train[key] = value
                elif int(layerPhase) == 1:
                    #for key, value in zip(blobNames[layerId]['top'] + ['label'], caffeLayer):
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns_test[key] = value
            else:
                for ns in (ns_train,ns_test):
                    caffeLayer = get_iterable(L.Input(
                        input_param={'shape':{'dim':map(int,layerParams['dim'].split(','))}}))
                    #for key, value in zip(blobNames[layerId]['top'] + ['label'], caffeLayer):
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns[key] = value

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

            for ns in (ns_train,ns_test):
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

        elif (layerType == 'ReLU'):
            inplace = layerParams['inplace']
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.ReLU(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    in_place=inplace))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

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

            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Pooling(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    pooling_param=pooling_param))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

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

            for ns in (ns_train,ns_test):
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


        elif (layerType == 'SoftmaxWithLoss'):
            pass
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.SoftmaxWithLoss(# try L['SoftmaxWithLoss']
                    *([ns[x] for x in blobNames[layerId]['bottom']])))
                    #*([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'Accuracy'):
            pass

            if layerPhase is not None:
                caffeLayer = get_iterable(L.Accuracy(
                    *([ns[x] for x in blobNames[layerId]['bottom']]),
                    #*([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label]),
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
                for ns in (ns_train,ns_test):
                    caffeLayer = get_iterable(L.Accuracy(
                        *([ns[x] for x in blobNames[layerId]['bottom']])))
                        #*([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
                    for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                        ns[key] = value


        elif (layerType == 'Dropout'):
            # inplace dropout? caffe-tensorflow do not work
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Dropout(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    in_place=inplace))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'LRN'):
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.LRN(
                    *[ns[x] for x in blobNames[layerId]['bottom']]))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'Concat'):
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Concat(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    ntop=len(blobNames[layerId]['top'])))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'Softmax'):
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Softmax(
                    *([ns[x] for x in blobNames[layerId]['bottom']])))
                    #*([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

    train = str(ns_train.to_proto())
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

    return prototxt

@csrf_exempt
def exportToCaffe(request):
    if request.method == 'POST':

        net = yaml.safe_load(request.POST.get('net'))

        prototxt = convertNetToPrototxt(net)

        randomId=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)

        with open(BASE_DIR+'/cloudcvIde/media/prototxt/'+randomId+'.prototxt', 'w') as f:
            f.write(prototxt)

        return HttpResponse(
            json.dumps({'id': randomId, 'name': randomId+'.prototxt', 'url': '/media/prototxt/'+randomId+'.prototxt'}),
            content_type="application/json")

@csrf_exempt
def exportToTensorflow(request):
    if request.method == 'POST':

        net = yaml.safe_load(request.POST.get('net'))
        prototxt = convertNetToPrototxt(net)

        randomId=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)

        with open(BASE_DIR+'/cloudcvIde/media/prototxt/'+randomId+'.prototxt', 'w') as f:
            f.write(prototxt)

        os.system('python '+BASE_DIR+'/cloudcvIde/caffe-tensorflow-master/convert.py '+BASE_DIR+'/cloudcvIde/media/prototxt/'+randomId+'.prototxt --code-output-path='+BASE_DIR+'/cloudcvIde/media/tensorflow/'+randomId+'.py')

        return HttpResponse(
            json.dumps({'id': randomId, 'name': randomId+'.py', 'url': '/media/tensorflow/'+randomId+'.py'}),
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
            elif(layer.type == 'Input'):
                params['dim'] = str(map(int,layer.input_param.shape[0].dim))[1:-1]
                # string '64,1,28,28'

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
