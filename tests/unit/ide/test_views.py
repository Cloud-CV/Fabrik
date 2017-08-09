import caffe
import json
import os
import sys
import unittest
import yaml

from caffe import layers as L, to_proto
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client
from ide.utils.jsonToPrototxt import json_to_prototxt
from ide.utils.shapes import get_shapes
from keras.models import model_from_json


# ********** Data Layers Test **********
class ImageDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['ImageData']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'ImageData')
        # Test 2
        net['l0']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'ImageData')
        # Test 3
        net['l0']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'ImageData')


class DataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Data']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'Data')
        # Test 2
        net['l0']['info']['phase'] = 0
        net['l0']['params']['mean_value'] = ''
        net['l0']['params']['mean_file'] = '/path/to/mean/file'
        net['l0']['params']['backend'] = "LEVELDB"
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'Data')
        # Test 3
        net['l0']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'Data')


class HDF5DataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['HDF5Data']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'HDF5Data')
        # Test 2
        net['l0']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'HDF5Data')
        # Test 3
        net['l0']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'HDF5Data')


class HDF5OutputLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['HDF5Output']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'HDF5Output')
        # Test 2
        net['l1']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'HDF5Output')
        # Test 3
        net['l1']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'HDF5Output')


class InputLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input']}
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertEqual(net['l0']['info']['type'], 'Input')


class WindowDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['WindowData']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'WindowData')
        # Test 2
        net['l0']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'WindowData')
        # Test 3
        net['l0']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'WindowData')


class MemoryDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['MemoryData']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'MemoryData')
        # Test 2
        net['l0']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'MemoryData')
        # Test 3
        net['l0']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'MemoryData')


class DummyDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['DummyData']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'DummyData')
        # Test 2
        net['l0']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'DummyData')
        # Test 3
        net['l0']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'DummyData')


# ********** Vision Layers Test **********
class ConvolutionLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Convolution']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Convolution')


class PoolingLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Pooling']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Pooling')
        # Test 2
        net['l1']['params']['pool'] = 'AVE'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Pooling')
        # Test 3
        net['l1']['params']['pool'] = 'STOCHASTIC'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Pooling')


class SPPLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['SPP']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'SPP')


class CropLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Crop']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Crop')


class DeconvolutionLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Deconvolution']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Deconvolution')


# ********** Recurrent Layers Test **********
class RecurrentLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Recurrent']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Recurrent')


class RNNLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['RNN']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'RNN')


class LSTMLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['LSTM']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'LSTM')


# ********** Common Layers Test **********
class InnerProductLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['InnerProduct']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'InnerProduct')


class DropoutLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Dropout']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Dropout')


class EmbedLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Embed']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Embed')


# ********** Normalisation Layers Test **********
class LRNLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['LRN']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'LRN')
        # Test 2
        net['l1']['params']['norm_region'] = 'ACROSS_CHANNELS'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'LRN')


class MVNLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['MVN']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'MVN')


class BatchNormLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['BatchNorm']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'BatchNorm')


# ********** Activation / Neuron Layers Test **********
class ReLULayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ReLU']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'ReLU')


class PReLULayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['PReLU']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'PReLU')


class ELULayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ELU']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'ELU')


class SigmoidLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Sigmoid']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Sigmoid')


class TanHLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['TanH']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'TanH')


class AbsValLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['AbsVal']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'AbsVal')


class PowerLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Power']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Power')


class ExpLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Exp']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Exp')


class LogLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Log']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Log')


class BNLLLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['BNLL']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'BNLL')


class ThresholdLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Threshold']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Threshold')


class BiasLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Bias']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Bias')


class ScaleLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Scale']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Scale')


# ********** Utility Layers Test **********
class FlattenLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Flatten']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Flatten')


class ReshapeLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Reshape']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Reshape')


class BatchReindexLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['BatchReindex']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'BatchReindex')


class SplitLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Split']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Split')


class ConcatLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Concat']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Concat')


class SliceLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Slice']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Slice')


class EltwiseLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Eltwise']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Eltwise')
        # Test 2
        net['l1']['params']['layer_type'] = 'Sum'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Eltwise')
        # Test 3
        net['l1']['params']['layer_type'] = 'Maximum'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Eltwise')
        # Test 4
        net['l1']['params']['layer_type'] = ''
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Eltwise')


class FilterLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Filter']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Filter')


# This layer is currently not supported as there is no bottom blob
'''class ParameterLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        data = L.Input(shape={'dim': [10, 3, 224, 224]})
        top = L.Parameter(data, shape={'dim': [10, 3, 224, 224]})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        with open('/home/utsav/Fabrik_Tests/ImageData.json', 'w') as outfile:
            json.dump(response, outfile)
        net = yaml.safe_load(json.dumps(response['net']))
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'ImageData')'''


class ReductionLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Reduction']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Reduction')
        # Test 2
        net['l1']['params']['operation'] = 'SUM'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Reduction')
        # Test 3
        net['l1']['params']['operation'] = 'ASUM'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Reduction')
        # Test 4
        net['l1']['params']['operation'] = 'SUMSQ'
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Reduction')


class SilenceLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Silence']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Silence')


class ArgMaxLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ArgMax']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'ArgMax')


class SoftmaxLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Softmax']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Softmax')


# ********** Loss Layers Test **********
class MultinomialLogisticLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['MultinomialLogisticLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'MultinomialLogisticLoss')


class InfogainLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['InfogainLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'InfogainLoss')


class SoftmaxWithLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['SoftmaxWithLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'SoftmaxWithLoss')


class EuclideanLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['EuclideanLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'EuclideanLoss')


class HingeLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['HingeLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'HingeLoss')


class SigmoidCrossEntropyLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['SigmoidCrossEntropyLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'SigmoidCrossEntropyLoss')


class AccuracyLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Accuracy']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Accuracy')
        # Test 2
        net['l1']['info']['phase'] = 0
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Accuracy')
        # Test 3
        net['l1']['info']['phase'] = 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Accuracy')


class ContrastiveLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ContrastiveLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'ContrastiveLoss')


# ********** Python Layer Test **********
class PythonDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['PythonData']}
        # Test 1
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'Python')
        # Test 2
        net['l0']['params']['endPoint'] = "1, 0"
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l0']['info']['type'], 'Python')


class PythonLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['PythonLoss']}
        net['l0']['connection']['output'].append('l1')
        prototxt, input_dim = json_to_prototxt(net, response['net_name'])
        self.assertGreater(len(prototxt), 9)
        self.assertEqual(net['l1']['info']['type'], 'Python')


# ********** Shape Calculation Test **********
class ShapeCalculationTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def caffe_test(self, path, key, success, layer=None):
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r') as f:
            response = self.client.post(reverse('caffe-import'), {'file': f})
        response = json.loads(response.content)
        if success:
            net = get_shapes(response['net'])
            caffe_net = caffe.Net(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), caffe.TEST)
            self.assertEqual(list(caffe_net.blobs[key].data.shape[1:]), net['l0']['shape']['output'])
        else:
            try:
                net = get_shapes(response['net'])
            except:
                message = 'Cannot determine shape of ' + layer + ' layer.'
                self.assertEqual(str(sys.exc_info()[1]), message)

    def keras_test(self, filename):
        with open(filename, 'r') as f:
            response = self.client.post(reverse('keras-import'), {'file': f})
        response = json.loads(response.content)
        net = get_shapes(response['net'])
        with open(filename, 'r') as f:
            model = model_from_json(json.dumps(json.load(f)))
        for layer in model.layers:
            self.assertEqual(list(layer.output_shape[::-1][:-1]), net[layer.name]['shape']['output'])

    def test_shapes(self):
        # Test 1
        image_path = os.path.join(settings.BASE_DIR, 'media', 'image_list.txt')
        data, _ = L.ImageData(source=image_path, batch_size=32, ntop=2, rand_skip=0,
                              shuffle=False, new_height=256, new_width=256, is_color=True,
                              root_folder=os.path.join(settings.BASE_DIR, 'example/'),
                              transform_param=dict(crop_size=227), name='l0')
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data)))
        self.caffe_test(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'ImageData1', True)
        # Test 2
        image_path = os.path.join(settings.BASE_DIR, 'media', 'image_list.txt')
        data, _ = L.ImageData(source=image_path, batch_size=32, ntop=2, rand_skip=0,
                              shuffle=False, new_height=256, new_width=256, is_color=True,
                              root_folder=os.path.join(settings.BASE_DIR, 'example/'), name='l0')
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data)))
        self.caffe_test(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'ImageData1', True)
        # Test 3
        data, _ = L.MemoryData(batch_size=32, ntop=2, channels=3, height=224, width=224)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data)))
        self.caffe_test(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'MemoryData1', True)
        # Test 4
        data, _ = L.HDF5Data(source='/dummy/source/', batch_size=32, ntop=2, shuffle=False)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data)))
        self.caffe_test(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'HDF5Data1', False,
                        'HDF5Data')
        # Test 5
        top = L.Python(module='pascal_multilabel_datalayers', layer='PascalMultilabelDataLayerSync',
                       param_str="{\'pascal_root\': \'../data/pascal/VOC2007\', \'im_shape\': [227, 227], \
                        \'split\': \'train\', \'batch_size\': 128}")
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        self.caffe_test(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'HDF5Data1', False,
                        'Python')
        # Test 6
        self.keras_test(os.path.join(settings.BASE_DIR, 'example/keras', 'shapeCheck1D.json'))
        # Test 7
        self.keras_test(os.path.join(settings.BASE_DIR, 'example/keras', 'shapeCheck2D.json'))
        # Test 8
        self.keras_test(os.path.join(settings.BASE_DIR, 'example/keras', 'shapeCheck3D.json'))
