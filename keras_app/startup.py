import os
from custom_layers import config


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)))


def run():
    for key, layer in config.config.iteritems():
        os.system('cp ' + BASE_DIR + '/keras_app/custom_layers/' + layer['filename'] + ' '
                  + BASE_DIR + '/media')
