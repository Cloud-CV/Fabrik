import json
import yaml
import urlparse
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from caffe_app.models import Network, NetworkVersion
from datetime import datetime


def create_network_version(network, netObj, tag):
    # creating a unique version of network to allow revert and view hitory
    network_version = NetworkVersion(network=netObj, tag=tag)
    network_version.network_def = network
    network_version.save()
    return network_version


@channel_session_user_from_http
def ws_connect(message):
    print('connection being established...')
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
    print('disconnected...')


@channel_session_user
def ws_receive(message):
    print('message received...')
    # param initialization
    data = yaml.safe_load(message['text'])
    networkId = message.channel_session['networkId']
    net = data['net']
    action = data['action']
    nextLayerId = data['nextLayerId']
    tag = data['message']

    # save changes to database to maintain consistency
    # get the net object on which update is made
    netObj = Network.objects.get(id=int(networkId))
    # network object is stored as string in db, when loading it is parsed
    # create a new version of network in order to allow history support
    network_version = create_network_version(json.dumps(net), netObj, tag)

    # modify last updated time
    netObj.updated_on = datetime.now()
    netObj.save()
    # sending update made by one user over all the sessions of open network
    # Note - conflict resolution still pending
    Group('model-{0}'.format(networkId)).send({
        'text': json.dumps({
            'net': net,
            'nextLayerId': nextLayerId,
            'action': action,
            'version_id': network_version.id
        })
    })
