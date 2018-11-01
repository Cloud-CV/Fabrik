import json
import yaml
import six.moves.urllib.parse as urlparse
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


@channel_session_user_from_http
def ws_connect(message):
    print('connection being established...')
    message.reply_channel.send({
        'accept': True
    })
    # extracting id of network from url params
    params = urlparse.parse_qs(message.content['query_string'])
    networkId = params.get('id', ('NotSupplied',))[0]
    message.channel_session['networkId'] = networkId
    # adding socket to a group based on networkId to send updates of network
    Group('model-{0}'.format(networkId)).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    networkId = message.channel_session['networkId']
    Group('model-{0}'.format(networkId)).discard(message.reply_channel)
    print('disconnected...')


@channel_session_user
def ws_receive(message):
    print('message received...')
    # param initialization
    data = yaml.safe_load(message['text'])
    action = data['action']

    if ('randomId' in data):
        randomId = data['randomId']

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
        add_highlight_to = data['addHighlightTo']
        remove_highlight_from = data['removeHighlightFrom']
        user_id = data['userId']
        highlight_color = data['highlightColor']
        username = data['username']

        Group('model-{0}'.format(networkId)).send({
            'text': json.dumps({
                'addHighlightTo': add_highlight_to,
                'removeHighlightFrom': remove_highlight_from,
                'userId': user_id,
                'action': action,
                'randomId': randomId,
                'highlightColor': highlight_color,
                'username': username
            })
        })
    else:
        # save changes to database to maintain consistency
        # get the net object on which update is made
        netObj = Network.objects.get(id=int(networkId))
        network_version = fetch_network_version(netObj)

        if (action == 'UpdateParam'):
            updated_data = {}
            updated_data['layerId'] = data['layerId']
            updated_data['param'] = data['param']
            updated_data['value'] = data['value']
            updated_data['isProp'] = data['isProp']
            updated_data['nextLayerId'] = data['nextLayerId']

            network_update = create_network_update(network_version, json.dumps(updated_data), data['action'])
            network_update.save()
            # sending update made by one user over all the sessions of open network
            # Note - conflict resolution still pending
            Group('model-{0}'.format(networkId)).send({
                'text': json.dumps({
                    'layerId': updated_data['layerId'],
                    'param': updated_data['param'],
                    'value': updated_data['value'],
                    'isProp': updated_data['isProp'],
                    'action': action,
                    'version_id': 0,
                    'randomId': randomId
                })
            })
        elif (data['action'] == 'DeleteLayer'):
            updated_data = {}
            updated_data['layerId'] = data['layerId']
            updated_data['nextLayerId'] = data['nextLayerId']

            network_update = create_network_update(network_version, json.dumps(updated_data), data['action'])
            network_update.save()

            # Note - conflict resolution still pending
            Group('model-{0}'.format(networkId)).send({
                'text': json.dumps({
                    'layerId': updated_data['layerId'],
                    'action': action,
                    'version_id': 0,
                    'randomId': randomId
                })
            })
        elif (action == 'AddLayer'):
            updated_data = {}
            updated_data['prevLayerId'] = data['prevLayerId']
            updated_data['layer'] = data['layer']
            updated_data['layerId'] = data['layerId']
            updated_data['nextLayerId'] = data['nextLayerId']

            network_update = create_network_update(network_version, json.dumps(updated_data), data['action'])
            network_update.save()
            # sending update made by one user over all the sessions of open network
            # Note - conflict resolution still pending
            Group('model-{0}'.format(networkId)).send({
                'text': json.dumps({
                    'layer': updated_data['layer'],
                    'prevLayerId': updated_data['prevLayerId'],
                    'action': action,
                    'version_id': 0,
                    'randomId': randomId
                })
            })
        elif (action == 'AddComment'):
            updated_data = {}
            updated_data['layerId'] = data['layerId']
            updated_data['comment'] = data['comment']

            network_update = create_network_update(network_version, json.dumps(updated_data), data['action'])
            network_update.save()

            Group('model-{0}'.format(networkId)).send({
                'text': json.dumps({
                    'layerId': updated_data['layerId'],
                    'comment': updated_data['comment'],
                    'action': action,
                    'version_id': 0,
                    'randomId': randomId
                })
            })
