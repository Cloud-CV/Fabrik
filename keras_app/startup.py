import os
from .custom_layers import config
import six

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)))


def run():
    for key, layer in six.iteritems(config.config):
        os.system(
            ('copy ' if os.name == 'nt' else 'cp ')
            + os.path.join(BASE_DIR, 'keras_app', 'custom_layers/', layer['filename'])
            + ' '
            + os.path.join(BASE_DIR, 'media')
        )
