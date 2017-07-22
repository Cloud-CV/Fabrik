import json
import os
import unittest
import yaml

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client
from keras.layers import Input
from keras.layers import Conv2D, Conv2DTranspose, ZeroPadding2D
from keras.layers import MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Activation, Dropout, Flatten, Reshape
from keras.layers import SimpleRNN, LSTM
from keras.layers import Embedding
from keras.layers import add, concatenate
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.layers import BatchNormalization
from keras.models import Model, Sequential
from keras import regularizers
from keras_app.views.layers_export import data, convolution, deconvolution, pooling, dense,\
    dropout, embed, recurrent, batchNorm, activation, flatten, reshape, concat, eltwise


class ImportJsonTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        sample_file = open(os.path.join(settings.BASE_DIR, 'example/keras', 'vgg16.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class ExportJsonTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        img_input = Input((224, 224, 3))
        model = Conv2D(64, (3, 3), padding='same', dilation_rate=1, use_bias=True,
                       kernel_regularizer=regularizers.l1(), bias_regularizer='l1',
                       activity_regularizer='l1', kernel_constraint='max_norm',
                       bias_constraint='max_norm')(img_input)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        response = self.client.post(reverse('keras-export'), {'net': json.dumps(response['net']),
                                                              'net_name': ''})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


# ********** Import json tests **********

# ********** Data Layers **********
class InputImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Input((224, 224, 3))
        model = Model(model, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[0]]['params']), 1)


# ********** Vision Layers **********
class ConvolutionImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = Conv2D(64, (3, 3), padding='same')(img_input)
        model = Activation('relu')(model)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[1]]['params']), 9)
        self.assertEqual(response['net'][layerId[0]]['info']['type'], 'ReLU')


class DeconvolutionImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = Conv2DTranspose(64, (3, 3), padding='same')(img_input)
        model = LeakyReLU()(model)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[0]]['params']), 9)
        self.assertEqual(response['net'][layerId[2]]['info']['type'], 'ReLU')


class PoolingImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = MaxPooling2D((2, 2), strides=(2, 2))(img_input)
        model = AveragePooling2D((2, 2), strides=(2, 2))(model)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[0]]['params']), 7)
        self.assertGreaterEqual(len(response['net'][layerId[2]]['params']), 7)


# ********** Common Layers **********
class DenseImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = Flatten()(img_input)
        model = Dense(100)(model)
        model = PReLU()(model)
        model = Dropout(0.5)(model)
        model = Reshape((1, 1, 100))(model)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[0]]['params']), 3)
        self.assertEqual(response['net'][layerId[2]]['info']['type'], 'Flatten')
        self.assertEqual(response['net'][layerId[4]]['info']['type'], 'PReLU')
        self.assertEqual(response['net'][layerId[5]]['info']['type'], 'Reshape')
        self.assertEqual(response['net'][layerId[1]]['info']['type'], 'Dropout')


class EmbeddingImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((100,))
        model = Embedding(100, 1000)(img_input)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[0]]['params']), 3)


# ********** Recurrent Layers **********
class RecurrentImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Embedding(100, output_dim=256))
        model.add(LSTM(32, return_sequences=True))
        model.add(SimpleRNN(64))
        model.build()
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[3]]['params']), 3)
        self.assertGreaterEqual(len(response['net'][layerId[5]]['params']), 3)


# ********** Normalisation Layers **********
class BatchNormImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = BatchNormalization(center=True, scale=True)(img_input)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net'][layerId[0]]['info']['type'], 'Scale')
        self.assertEqual(response['net'][layerId[1]]['info']['type'], 'BatchNorm')


# ********** Utility Layers **********
class PaddingImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = ZeroPadding2D((3, 3))(img_input)
        model = Conv2D(64, (7, 7), strides=(2, 2))(model)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net'][layerId[0]]['params']['pad_h'], 3)


class EltwiseImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 64))
        model = Conv2D(64, (3, 3), padding='same')(img_input)
        model = add([img_input, model])
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net'][layerId[0]]['params']['layer_type'], 'Sum')


class ConcatImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = Conv2D(64, (3, 3), padding='same')(img_input)
        model = concatenate([img_input, model])
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net'][layerId[0]]['info']['type'], 'Concat')


# ********** Export json tests **********

# ********** Data Layers Test **********
class InputExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input']}
        net = data(net['l0'], '', 'l0')
        model = Model(net['l0'], net['l0'])
        self.assertEqual(model.layers[0].__class__.__name__, 'InputLayer')


# ********** Vision Layers Test **********
class ConvolutionExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Convolution']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = convolution(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Conv2D')


class PoolingExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Pooling']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = pooling(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'AveragePooling2D')


class DeconvolutionExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Deconvolution']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = deconvolution(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Conv2DTranspose')


# ********** Recurrent Layers Test **********
class RNNExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input2'], 'l1': net['RNN']}
        net['l0']['connection']['output'].append('l1')
        # # net = get_shapes(net)
        inp = data(net['l0'], '', 'l0')['l0']
        net = recurrent(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'SimpleRNN')


class LSTMExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input2'], 'l1': net['LSTM']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = recurrent(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'LSTM')


# ********** Common Layers Test **********
class DenseExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input3'], 'l1': net['InnerProduct']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = dense(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Dense')


class DropoutExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input3'], 'l1': net['Dropout']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = dropout(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Dropout')


class EmbedExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input3'], 'l1': net['Embed']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = embed(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Embedding')


# ********** Normalisation Layers Test **********
class BatchNormExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['BatchNorm'], 'l2': net['Scale']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = batchNorm(net['l1'], [inp], 'l1', 'l2', net['l2'])
        model = Model(inp, net['l2'])
        self.assertEqual(model.layers[1].__class__.__name__, 'BatchNormalization')


# ********** Activation / Neuron Layers Test **********
class ReLUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ReLU']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


class PReLUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['PReLU']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'PReLU')


class ELUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ELU']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'ELU')


class SigmoidExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Sigmoid']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


class TanHExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['TanH']}
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


# ********** Utility Layers Test **********
class FlattenExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Flatten']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = flatten(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Flatten')


class ReshapeExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Reshape']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = reshape(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Reshape')


class ConcatExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Concat']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = concat(net['l1'], [inp, inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Concatenate')


class EltwiseExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Eltwise']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = eltwise(net['l1'], [inp, inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Maximum')


class SoftmaxExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_to_prototxt(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Softmax']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')
