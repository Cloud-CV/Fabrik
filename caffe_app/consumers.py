import json
import yaml
import urlparse
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from caffe_app.models import Network, NetworkVersion, NetworkUpdates
from ide.views import get_network_version
from ide.tasks import export_caffe_prototxt, export_keras_json


def create_network_version(network, netObj):
    # creating a unique version of network to allow revert and view hitory
    network_version = NetworkVersion(network=netObj)
    network_version.network_def = network
    network_version.save()
    return network_version


def create_network_update(network_version, updated_data, tag):
    network_update = NetworkUpdates(network_version=network_version,
                                    updated_data=updated_data,
                                    tag=tag)
    return network_update


def fetch_network_version(netObj):
    network_version = NetworkVersion.objects.filter(network=netObj).order_by('-created_on')[0]
    updates_batch = NetworkUpdates.objects.filter(network_version=network_version)

    # Batching updates
    # Note - size of batch is 20 for now, optimization can be done
    if len(updates_batch) == 2:
        data = get_network_version(netObj)
        network_version = NetworkVersion(network=netObj, network_def=json.dumps(data['network']))
        network_version.save()

        network_update = NetworkUpdates(network_version=network_version,
                                        updated_data=json.dumps({'nextLayerId': data['next_layer_id']}),
                                        tag='CheckpointCreated')
        network_update.save()
    return network_version


def update_data(data, required_data, version_id=0):
    '''
        Parses data to include only required keys and returns the required object
    '''

    updated_data = {key: data[key] for key in required_data}
    group_data = updated_data.copy()
    group_data['action'] = data['action']

    if ('randomId' in data):
        group_data['randomId'] = data['randomId']
    group_data['version_id'] = version_id

    group_data = {"text": json.dumps(group_data)}

    return updated_data, group_data


@channel_session_user_from_http
def ws_connect(message):
    print('Connection being established...')
    message.reply_channel.send({
        'accept': True
    })
    # extracting id of network from url params
    params = urlparse.parse_qs(message.content['query_string'])
    networkId = params.get('id', ('Not Supplied',))[0]
    message.channel_session['networkId'] = networkId
    # adding socket to a group based on networkId to send updates of network
    Group('model-{0}'.format(networkId)).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    networkId = message.channel_session['networkId']
    Group('model-{0}'.format(networkId)).discard(message.reply_channel)
    print('Disconnected...')


@channel_session_user
def ws_receive(message):
    print('Message received...')
    # param initialization
    data = yaml.safe_load(message['text'])
    action = data['action']

    update_params = {
        'UpdateHighlight': ['addHighlightTo', 'removeHighlightFrom', 'userId', 'highlightColor', 'username'],
        'UpdateParam': ['layerId', 'param', 'value', 'isProp'],
        'DeleteLayer': ['layerId'],
        'AddLayer': ['layer', 'layerId', 'prevLayerId', 'nextLayerId'],
        'AddComment': ['layerId', 'comment']
    }

    if ('networkId' in message.channel_session):
        networkId = message.channel_session['networkId']

    if (action == 'ExportNet'):
        # async export call
        framework = data['framework']
        net = data['net']
        net_name = data['net_name']

        reply_channel = message.reply_channel.name

        if (framework == 'caffe'):
            export_caffe_prototxt.delay(net, net_name, reply_channel)
        elif (framework == 'keras'):
            export_keras_json.delay(net, net_name, False, reply_channel)
        elif (framework == 'tensorflow'):
            export_keras_json.delay(net, net_name, True, reply_channel)

    elif (action == 'UpdateHighlight'):
        group_data = update_data(data, update_params['UpdateHighlight'])[1]

        Group('model-{0}'.format(networkId)).send(group_data)
    elif (action in update_params):
        # get the net object on which update is made
        netObj = Network.objects.get(id=int(networkId))
        network_version = fetch_network_version(netObj)

        updated_data, group_data = update_data(data, update_params[action])

        network_update = create_network_update(network_version, json.dumps(updated_data), data['action'])
        network_update.save()

        Group('model-{0}'.format(networkId)).send(group_data)
