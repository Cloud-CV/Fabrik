import copy
import sys
import yaml

from yaml import safe_load
from caffe_app.models import Network, NetworkVersion
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from utils.shapes import get_shapes, get_layer_shape, handle_concat_layer
from django.db.models import Max


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def fetch_layer_shape(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        layerId = request.POST.get('layerId')
        try:
            net[layerId]['shape'] = {}
            net[layerId]['shape']['input'] = None
            net[layerId]['shape']['output'] = None
            dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData']

            # Obtain input shape of new layer
            if (net[layerId]['info']['type'] == "Concat"):
                for parentLayerId in net[layerId]['connection']['input']:
                    # Check if parent layer have shapes
                    if (net[parentLayerId]['shape']['output']):
                        net[layerId]['shape']['input'] = handle_concat_layer(net[layerId], net[parentLayerId])
            elif (not (net[layerId]['info']['type'] in dataLayers)):
                if (len(net[layerId]['connection']['input']) > 0):
                    parentLayerId = net[layerId]['connection']['input'][0]
                    # Check if parent layer have shapes
                    if (net[parentLayerId]['shape']['output']):
                        net[layerId]['shape']['input'] = net[parentLayerId]['shape']['output'][:]

            # Obtain output shape of new layer
            if (net[layerId]['info']['type'] in dataLayers):
                # handling Data Layers separately
                if ('dim' in net[layerId]['params'] and len(net[layerId]['params']['dim'])):
                    # layers with empty dim parameter can't be passed
                    net[layerId]['shape']['input'], net[layerId]['shape']['output'] =\
                            get_layer_shape(net[layerId])
                elif ('dim' not in net[layerId]['params']):
                    # shape calculation for layers with no dim param
                    net[layerId]['shape']['input'], net[layerId]['shape']['output'] =\
                            get_layer_shape(net[layerId])
            else:
                if (net[layerId]['shape']['input']):
                    net[layerId]['shape']['output'] = get_layer_shape(net[layerId])
        except BaseException:
            return JsonResponse({
                'result': 'error', 'error': str(sys.exc_info()[1])})
        return JsonResponse({'result': 'success', 'net': net})


@csrf_exempt
def calculate_parameter(request):
    if request.method == 'POST':
        net = yaml.safe_load(request.POST.get('net'))
        try:
            # While calling get_shapes we need to remove the flag
            # added in frontend to show the parameter on pane
            netObj = copy.deepcopy(net)
            for layerId in netObj:
                for param in netObj[layerId]['params']:
                    netObj[layerId]['params'][param] = netObj[layerId]['params'][param][0]
            # use get_shapes method to obtain shapes of each layer
            netObj = get_shapes(netObj)
            for layerId in net:
                net[layerId]['shape'] = {}
                net[layerId]['shape']['input'] = netObj[layerId]['shape']['input']
                net[layerId]['shape']['output'] = netObj[layerId]['shape']['output']
        except BaseException:
            return JsonResponse({
                'result': 'error', 'error': str(sys.exc_info()[1])})
        return JsonResponse({'result': 'success', 'net': net})


@csrf_exempt
def save_to_db(request):
    if request.method == 'POST':
        net = request.POST.get('net')
        net_name = request.POST.get('net_name')
        user_id = request.POST.get('user_id')
        public_sharing = True
        user = None
        if net_name == '':
            net_name = 'Net'
        try:
            # making model sharing public by default for now
            # TODO: Prvilege on Sharing
            if user_id:
                user_id = int(user_id)
                user = User.objects.get(id=user_id)

            # create a new model on share event
            model = Network(name=net_name, public_sharing=public_sharing, author=user)
            model.save()
            # create first version of model
            model_version = NetworkVersion(network=model, network_def=net)
            model_version.tag = 'Model created'
            model_version.save()

            return JsonResponse({'result': 'success', 'id': model.id})
        except:
            return JsonResponse({'result': 'error', 'error': str(sys.exc_info()[1])})


@csrf_exempt
def load_from_db(request):
    if request.method == 'POST':
        if 'proto_id' in request.POST:
            try:
                model = Network.objects.get(id=int(request.POST['proto_id']))
                version_id = None

                if 'version_id' in request.POST and request.POST['version_id'] != '':
                    # added for loading any previous version of model
                    version_id = int(request.POST['version_id'])
                else:
                    # find the latest version of model where network id is proto_id
                    version_id_dict = NetworkVersion.objects.filter(network=model) \
                                        .values('network').annotate(version_id=Max('id')) \
                                        .order_by()
                    version_id = version_id_dict[0]['version_id']

                # fetch the required version of model
                model_version = NetworkVersion.objects.get(id=version_id)
                net = safe_load(model_version.network_def)

                # authorizing the user for access to model
                if not model.public_sharing:
                    return JsonResponse({'result': 'error',
                                         'error': 'Permission denied for access to model'})
            except Exception:
                return JsonResponse({'result': 'error',
                                     'error': 'No network file found'})
            return JsonResponse({'result': 'success', 'net': net, 'net_name': model.name})

    if request.method == 'GET':
        return index(request)


@csrf_exempt
def fetch_model_history(request):
    if request.method == 'POST':
        try:
            network_id = int(request.POST['net_id'])
            network = Network.objects.get(id=network_id)
            network_versions = NetworkVersion.objects.filter(network=network)

            modelHistory = {}
            for version in network_versions:
                modelHistory[version.id] = version.tag

            return JsonResponse({
                'result': 'success',
                'data': modelHistory
            })
        except Exception:
            return JsonResponse({
                'result': 'error',
                'error': 'Unable to load model history'
            })
