import collections
import caffe
from caffe import layers as L
import re

def jsonToPrototxt(net,net_name):
    # assumption: a layer can accept only one input blob
    # the data layer produces two blobs: data and label
    # the loss layer requires two blobs: <someData> and label
    # the label blob is hardcoded.
    # layers name have to be unique

    # custom DFS of the network
    input_dim = None;

    def get_iterable(x):
        if isinstance(x, collections.Iterable):
            return x
        else:
            return (x,)

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
        if(net[layerId]['info']['type'] == 'Data' or net[layerId]['info']['type'] == 'Input' 
            or net[layerId]['info']['type'] == 'HDF5Data'):
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

            input_dim = layerParams['dim']

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

        elif (layerType == 'Crop'):
            crop_param={}

            if layerParams['axis'] != '':
                crop_param['axis'] = int(float(layerParams['axis']))
            if layerParams['offset'] != '':
                crop_param['offset'] = int(float(layerParams['offset']))

            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Crop(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    crop_param=crop_param))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value



        elif (layerType == 'Convolution'):

            convolution_param={}
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

        elif (layerType == 'Deconvolution'):

            convolution_param={}
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
                convolution_param['weight_filler']={}
                convolution_param['weight_filler']['type'] = layerParams['weight_filler']
            if layerParams['bias_filler'] != '':
                convolution_param['bias_filler']={}
                convolution_param['bias_filler']['type'] = layerParams['bias_filler']

            for ns in (ns_train,ns_test):
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
                if 'inplace' in layerParams.keys():
                    inplace = layerParams['inplace']
                else:
                    inplace = False
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

        elif (layerType == 'Eltwise'):
            eltwise_param={}
            if layerParams['operation'] != '':
                elt = layerParams['operation']
                if(elt == 'PROD'):
                    elt = 0
                elif(elt == 'SUM'):
                    elt = 1
                elif(elt == 'MAX'):
                    elt = 2
            else:
                elt = 1 #Default is sum
            eltwise_param['operation'] = elt
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Eltwise(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    eltwise_param=eltwise_param))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'Softmax'):
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Softmax(
                    *([ns[x] for x in blobNames[layerId]['bottom']])))
                    #*([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value
        
        elif (layerType == 'Embed'):
            for ns in (ns_train,ns_test):
                print ns.tops
                caffeLayer = get_iterable(L.Embed(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
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
                    #*([ns[x] for x in blobNames[layerId]['bottom']] + [ns.label])))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'LSTM'):
            recurrent_param = {}
            if layerParams['num_output'] != '':
                recurrent_param['num_output'] = int(layerParams['num_output'])
            if layerParams['weight_filler'] != '':
                recurrent_param['weight_filler'] = {
                    'type': layerParams['weight_filler']
                }
            if layerParams['bias_filler'] != '':
                recurrent_param['bias_filler'] = {
                    'type': layerParams['bias_filler']
                }
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.LSTM(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                        recurrent_param=recurrent_param))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'Reshape'):
            reshape_param={'shape':{'dim':map(int,layerParams['dim'].split(','))}}
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Reshape(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                        reshape_param=reshape_param))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value
        
        elif (layerType == 'HDF5Data'):
            layerPhase = layer['info']['phase']
            hdf5_data_param = {}
            if layerParams['source'] != '':
                hdf5_data_param['source'] = layerParams['source']
            if layerParams['batch_size'] != '':
                hdf5_data_param['batch_size'] = layerParams['batch_size']
            for ns in (ns_train,ns_test):
                if layerPhase is not None:
                    caffeLayer = get_iterable(L.HDF5Data(
                        *[ns[x] for x in blobNames[layerId]['bottom']],
                            hdf5_data_param=hdf5_data_param,
                            include={
                                'phase': int(layerPhase)
                            }))
                else:
                    caffeLayer = get_iterable(L.HDF5Data(
                        *[ns[x] for x in blobNames[layerId]['bottom']],
                            hdf5_data_param=hdf5_data_param))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value


        elif (layerType == 'BatchNorm'):
            batch_norm_param = {}
            if layerParams['use_global_stats'] != '':
                batch_norm_param['use_global_stats'] = layerParams['use_global_stats']
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.BatchNorm(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    batch_norm_param=batch_norm_param
                    ))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

        elif (layerType == 'Scale'):
            scale_param = {}
            if layerParams['bias_term'] != '':
                scale_param['bias_term'] = layerParams['bias_term']
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Scale(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    scale_param=scale_param
                    ))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value
        elif (layerType == 'Eltwise'):
            eltwise_param = {}
            if layerParams['operation'] != '':
                eltwise_param['operation'] = int(layerParams['operation'])
            for ns in (ns_train,ns_test):
                caffeLayer = get_iterable(L.Eltwise(
                    *[ns[x] for x in blobNames[layerId]['bottom']],
                    eltwise_param=eltwise_param
                    ))
                for key, value in zip(blobNames[layerId]['top'], caffeLayer):
                    ns[key] = value

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

    return prototxt,input_dim
