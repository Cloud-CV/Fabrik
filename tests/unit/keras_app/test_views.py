import json
import os
import unittest
import yaml

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Reshape, Permute, RepeatVector
from keras.layers import ActivityRegularization, Masking
from keras.layers import Conv1D, Conv2D, Conv3D, Conv2DTranspose
from keras.layers import UpSampling1D, UpSampling2D, UpSampling3D
from keras.layers import GlobalMaxPooling1D, GlobalMaxPooling2D
from keras.layers import MaxPooling1D, MaxPooling2D, MaxPooling3D
from keras.layers import ZeroPadding1D, ZeroPadding2D, ZeroPadding3D
from keras.layers import LocallyConnected1D, LocallyConnected2D
from keras.layers import SimpleRNN, LSTM, GRU
from keras.layers import Embedding
from keras.layers import add, concatenate
from keras.layers.advanced_activations import LeakyReLU, PReLU, \
    ELU, ThresholdedReLU
from keras.layers import BatchNormalization
from keras.layers import GaussianNoise, GaussianDropout, AlphaDropout
from keras.layers import Input
from keras import regularizers
from keras.models import Model, Sequential
from keras_app.views.layers_export import data, convolution, deconvolution, \
    pooling, dense, dropout, embed, recurrent, batch_norm, activation, \
    flatten, reshape, eltwise, concat, upsample, locally_connected, permute, \
    repeat_vector, regularization, masking, gaussian_noise, \
    gaussian_dropout, alpha_dropout
from ide.utils.shapes import get_shapes


class ImportJsonTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        # Test 1
        sample_file = open(os.path.join(settings.BASE_DIR,
                                        'example/keras',
                                        'vgg16.json'), 'r')
        response = self.client.post(reverse('keras-import'),
                                    {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
        # Test 2
        sample_file = open(os.path.join(settings.BASE_DIR,
                                        'example/caffe',
                                        'GoogleNet.prototxt'), 'r')
        response = self.client.post(reverse('keras-import'),
                                    {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'error')
        self.assertEqual(response['error'], 'Invalid JSON')

    def test_keras_import_sample_id(self):
        # Test 1
        response = self.client.post(
            reverse('keras-import'),
            {'sample_id': 'vgg16'})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net_name'], 'vgg16')
        self.assertTrue('net' in response)
        # Test 2
        response = self.client.post(
            reverse('keras-import'),
            {'sample_id': 'shapeCheck4D'})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'error')
        self.assertEqual(response['error'], 'No JSON model file found')


class ExportJsonTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        # Test 1
        img_input = Input((224, 224, 3))
        model = Conv2D(64, (3, 3), padding='same', dilation_rate=1, use_bias=True,
                       kernel_regularizer=regularizers.l1(), bias_regularizer='l1',
                       activity_regularizer='l1', kernel_constraint='max_norm',
                       bias_constraint='max_norm')(img_input)
        model = BatchNormalization(center=True, scale=True, beta_regularizer=regularizers.l2(0.01),
                                   gamma_regularizer=regularizers.l2(0.01),
                                   beta_constraint='max_norm', gamma_constraint='max_norm',)(model)
        model = Model(img_input, model)
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        net = get_shapes(response['net'])
        response = self.client.post(reverse('keras-export'), {'net': json.dumps(net),
                                                              'net_name': ''})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
        # Test 2
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'ide',
                                  'caffe_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['HDF5Data']}
        # Currently we can't determine shape of HDF5Data Layer
        response = self.client.post(reverse('keras-export'), {'net': json.dumps(net),
                                                              'net_name': ''})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'error')


# ********** Import json tests **********
class HelperFunctions():
    def setUp(self):
        self.client = Client()

    def keras_type_test(self, model, id, type):
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net'][layerId[id]]['info']['type'], type)

    def keras_param_test(self, model, id, params):
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[id]]['params']), params)


# ********** Data Layers **********
class InputImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Input((224, 224, 3))
        model = Model(model, model)
        self.keras_param_test(model, 0, 1)


# ********** Core Layers **********
class DenseImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Dense(100, kernel_regularizer=regularizers.l2(0.01), bias_regularizer=regularizers.l2(0.01),
                        activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                        bias_constraint='max_norm', activation='relu', input_shape=(16,)))
        model.build()
        self.keras_param_test(model, 1, 3)


class ActivationImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        # softmax
        model = Sequential()
        model.add(Activation('softmax', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'Softmax')
        # relu
        model = Sequential()
        model.add(Activation('relu', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'ReLU')
        # tanh
        model = Sequential()
        model.add(Activation('tanh', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'TanH')
        # sigmoid
        model = Sequential()
        model.add(Activation('sigmoid', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'Sigmoid')
        # selu
        model = Sequential()
        model.add(Activation('selu', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'SELU')
        # softplus
        model = Sequential()
        model.add(Activation('softplus', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'Softplus')
        # softsign
        model = Sequential()
        model.add(Activation('softsign', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'Softsign')
        # hard_sigmoid
        model = Sequential()
        model.add(Activation('hard_sigmoid', input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'HardSigmoid')
        # LeakyReLU
        model = Sequential()
        model.add(LeakyReLU(alpha=1, input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'ReLU')
        # PReLU
        model = Sequential()
        model.add(PReLU(input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'PReLU')
        # ELU
        model = Sequential()
        model.add(ELU(alpha=1, input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'ELU')
        # ThresholdedReLU
        model = Sequential()
        model.add(ThresholdedReLU(theta=1, input_shape=(15,)))
        model.build()
        self.keras_type_test(model, 0, 'ThresholdedReLU')


class DropoutImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Dropout(0.5, input_shape=(10, 64)))
        model.build()
        self.keras_type_test(model, 0, 'Dropout')


class FlattenImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Flatten(input_shape=(10, 64)))
        model.build()
        self.keras_type_test(model, 0, 'Flatten')


class ReshapeImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Reshape((5, 2), input_shape=(10,)))
        model.build()
        self.keras_type_test(model, 0, 'Reshape')


class PermuteImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Permute((2, 1), input_shape=(10, 64)))
        model.build()
        self.keras_type_test(model, 0, 'Permute')


class RepeatVectorImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(RepeatVector(3, input_shape=(10,)))
        model.build()
        self.keras_type_test(model, 0, 'RepeatVector')


class ActivityRegularizationImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(ActivityRegularization(l1=2, input_shape=(10,)))
        model.build()
        self.keras_type_test(model, 0, 'Regularization')


class MaskingImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Masking(mask_value=0., input_shape=(5, 100)))
        model.build()
        self.keras_type_test(model, 0, 'Masking')


# ********** Convolutional Layers **********
class ConvolutionImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        # Conv 1D
        model = Sequential()
        model.add(Conv1D(32, 3, kernel_regularizer=regularizers.l2(0.01),
                         bias_regularizer=regularizers.l2(0.01),
                         activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                         bias_constraint='max_norm', activation='relu', input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 1, 9)
        # Conv 2D
        model = Sequential()
        model.add(Conv2D(32, (3, 3), kernel_regularizer=regularizers.l2(0.01),
                         bias_regularizer=regularizers.l2(0.01),
                         activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                         bias_constraint='max_norm', activation='relu', input_shape=(1, 16, 16)))
        model.build()
        self.keras_param_test(model, 1, 13)
        # Conv 3D
        model = Sequential()
        model.add(Conv3D(32, (3, 3, 3), kernel_regularizer=regularizers.l2(0.01),
                         bias_regularizer=regularizers.l2(0.01),
                         activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                         bias_constraint='max_norm', activation='relu', input_shape=(1, 16, 16, 16)))
        model.build()
        self.keras_param_test(model, 1, 17)


# This is currently unavailable with Theano backend
'''
class DepthwiseConvolutionImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(SeparableConv2D(32, 3, depthwise_regularizer=regularizers.l2(0.01),
                                  pointwise_regularizer=regularizers.l2(0.01),
                                  bias_regularizer=regularizers.l2(0.01),
                                  activity_regularizer=regularizers.l2(0.01), depthwise_constraint='max_norm',
                                  bias_constraint='max_norm', pointwise_constraint='max_norm',
                                  activation='relu', input_shape=(1, 16, 16)))
        self.keras_param_test(model, 1, 12)'''


class DeconvolutionImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Conv2DTranspose(32, (3, 3), kernel_regularizer=regularizers.l2(0.01),
                                  bias_regularizer=regularizers.l2(0.01),
                                  activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                                  bias_constraint='max_norm', activation='relu', input_shape=(1, 16, 16)))
        model.build()
        self.keras_param_test(model, 1, 13)


class UpsampleImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        # Upsample 1D
        model = Sequential()
        model.add(UpSampling1D(size=2, input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 0, 2)
        # Upsample 2D
        model = Sequential()
        model.add(UpSampling2D(size=(2, 2), input_shape=(1, 16, 16)))
        model.build()
        self.keras_param_test(model, 0, 3)
        # Upsample 3D
        model = Sequential()
        model.add(UpSampling3D(size=(2, 2, 2), input_shape=(1, 16, 16, 16)))
        model.build()
        self.keras_param_test(model, 0, 4)


# ********** Pooling Layers **********
class PoolingImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        # Global Pooling 1D
        model = Sequential()
        model.add(GlobalMaxPooling1D(input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 0, 5)
        # Global Pooling 2D
        model = Sequential()
        model.add(GlobalMaxPooling2D(input_shape=(1, 16, 16)))
        model.build()
        self.keras_param_test(model, 0, 8)
        # Pooling 1D
        model = Sequential()
        model.add(MaxPooling1D(pool_size=2, strides=2, padding='same', input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 0, 5)
        # Pooling 2D
        model = Sequential()
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same', input_shape=(1, 16, 16)))
        model.build()
        self.keras_param_test(model, 0, 8)
        # Pooling 3D
        model = Sequential()
        model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2), padding='same',
                               input_shape=(1, 16, 16, 16)))
        model.build()
        self.keras_param_test(model, 0, 11)


# ********** Locally-connected Layers **********
class LocallyConnectedImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        # Conv 1D
        model = Sequential()
        model.add(LocallyConnected1D(32, 3, kernel_regularizer=regularizers.l2(0.01),
                                     bias_regularizer=regularizers.l2(0.01),
                                     activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                                     bias_constraint='max_norm', activation='relu', input_shape=(10, 16)))
        model.build()
        self.keras_param_test(model, 1, 12)
        # Conv 2D
        model = Sequential()
        model.add(LocallyConnected2D(32, (3, 3), kernel_regularizer=regularizers.l2(0.01),
                                     bias_regularizer=regularizers.l2(0.01),
                                     activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                                     bias_constraint='max_norm', activation='relu', input_shape=(10, 16, 16)))
        model.build()
        self.keras_param_test(model, 1, 14)


# ********** Recurrent Layers **********
class RecurrentImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(LSTM(64, return_sequences=True, input_shape=(10, 64)))
        model.add(SimpleRNN(32, return_sequences=True))
        model.add(GRU(10, kernel_regularizer=regularizers.l2(0.01),
                      bias_regularizer=regularizers.l2(0.01), recurrent_regularizer=regularizers.l2(0.01),
                      activity_regularizer=regularizers.l2(0.01), kernel_constraint='max_norm',
                      bias_constraint='max_norm', recurrent_constraint='max_norm'))
        model.build()
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertGreaterEqual(len(response['net'][layerId[1]]['params']), 7)
        self.assertGreaterEqual(len(response['net'][layerId[3]]['params']), 7)
        self.assertGreaterEqual(len(response['net'][layerId[6]]['params']), 7)


# ********** Embedding Layers **********
class EmbeddingImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(Embedding(1000, 64, input_length=10, embeddings_regularizer=regularizers.l2(0.01),
                            embeddings_constraint='max_norm'))
        model.build()
        self.keras_param_test(model, 0, 7)


# ********** Merge Layers **********
class ConcatImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 3))
        model = Conv2D(64, (3, 3), padding='same')(img_input)
        model = concatenate([img_input, model])
        model = Model(img_input, model)
        self.keras_type_test(model, 0, 'Concat')


class EltwiseImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        img_input = Input((224, 224, 64))
        model = Conv2D(64, (3, 3), padding='same')(img_input)
        model = add([img_input, model])
        model = Model(img_input, model)
        self.keras_type_test(model, 0, 'Eltwise')


# ********** Normalisation Layers **********
class BatchNormImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(BatchNormalization(center=True, scale=True, beta_regularizer=regularizers.l2(0.01),
                                     gamma_regularizer=regularizers.l2(0.01),
                                     beta_constraint='max_norm', gamma_constraint='max_norm',
                                     input_shape=(10, 16)))
        model.build()
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


# ********** Noise Layers **********
class GaussianNoiseImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(GaussianNoise(stddev=0.1, input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 0, 1)


class GaussianDropoutImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(GaussianDropout(rate=0.5, input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 0, 1)


class AlphaDropoutImportTest(unittest.TestCase, HelperFunctions):
    def setUp(self):
        self.client = Client()

    def test_keras_import(self):
        model = Sequential()
        model.add(AlphaDropout(rate=0.5, seed=5, input_shape=(1, 16)))
        model.build()
        self.keras_param_test(model, 0, 1)


# ********** Utility Layers **********
class PaddingImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def pad_test(self, model, field, value):
        json_string = Model.to_json(model)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'w') as out:
            json.dump(json.loads(json_string), out, indent=4)
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': sample_file})
        response = json.loads(response.content)
        layerId = sorted(response['net'].keys())
        self.assertEqual(response['result'], 'success')
        self.assertEqual(response['net'][layerId[0]]['params'][field], value)

    def test_keras_import(self):
        # Pad 1D
        model = Sequential()
        model.add(ZeroPadding1D(2, input_shape=(224, 3)))
        model.add(Conv1D(32, 7, strides=2))
        model.build()
        self.pad_test(model, 'pad_w', 2)
        # Pad 2D
        model = Sequential()
        model.add(ZeroPadding2D(2, input_shape=(224, 224, 3)))
        model.add(Conv2D(32, 7, strides=2))
        model.build()
        self.pad_test(model, 'pad_w', 2)
        # Pad 3D
        model = Sequential()
        model.add(ZeroPadding3D(2, input_shape=(224, 224, 224, 3)))
        model.add(Conv3D(32, 7, strides=2))
        model.build()
        self.pad_test(model, 'pad_w', 2)


# ********** Export json tests **********

# ********** Data Layers Test **********
class InputExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input']}
        net = data(net['l0'], '', 'l0')
        model = Model(net['l0'], net['l0'])
        self.assertEqual(model.layers[0].__class__.__name__, 'InputLayer')


# ********** Core Layers **********
class DenseExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input2'], 'l1': net['InnerProduct']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        inp = data(net['l0'], '', 'l0')['l0']
        temp = dense(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Dense')
        # Test 2
        net['l1']['params']['weight_filler'] = 'glorot_normal'
        net['l1']['params']['bias_filler'] = 'glorot_normal'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = dense(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Dense')


class ReLUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ReLU']}
        # Test 1
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        temp = activation(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')
        # Test 2
        net['l1']['params']['negative_slope'] = 1
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        temp = activation(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'LeakyReLU')


class PReLUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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

    def test_keras_export(self):
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


class ThresholdedReLUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['ThresholdedReLU']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'ThresholdedReLU')


class SigmoidExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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

    def test_keras_export(self):
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


class SoftmaxExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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


class SELUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['SELU']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


class SoftplusExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Softplus']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


class SoftsignExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Softsign']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


class HardSigmoidExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['HardSigmoid']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = activation(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Activation')


class DropoutExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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


class FlattenExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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

    def test_keras_export(self):
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


class PermuteExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input2'], 'l1': net['Permute']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = permute(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Permute')


class RepeatVectorExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input3'], 'l1': net['RepeatVector']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = repeat_vector(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'RepeatVector')


class RegularizationExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input3'], 'l1': net['Regularization']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = regularization(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'ActivityRegularization')


class MaskingExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input2'], 'l1': net['Masking']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = masking(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Masking')


# ********** Vision Layers Test **********
class ConvolutionExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Input2'], 'l2': net['Input4'], 'l3': net['Convolution']}
        # Conv 1D
        net['l1']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l1']
        net['l3']['params']['layer_type'] = '1D'
        net['l3']['shape']['input'] = net['l1']['shape']['output']
        net['l3']['shape']['output'] = [128, 12]
        inp = data(net['l1'], '', 'l1')['l1']
        temp = convolution(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Conv1D')
        # Conv 2D
        net['l0']['connection']['output'].append('l0')
        net['l3']['connection']['input'] = ['l0']
        net['l3']['params']['layer_type'] = '2D'
        net['l3']['shape']['input'] = net['l0']['shape']['output']
        net['l3']['shape']['output'] = [128, 226, 226]
        inp = data(net['l0'], '', 'l0')['l0']
        temp = convolution(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Conv2D')
        # Conv 3D
        net['l2']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l2']
        net['l3']['params']['layer_type'] = '3D'
        net['l3']['shape']['input'] = net['l2']['shape']['output']
        net['l3']['shape']['output'] = [128, 226, 226, 18]
        inp = data(net['l2'], '', 'l2')['l2']
        temp = convolution(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Conv3D')


class DeconvolutionExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Deconvolution']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        inp = data(net['l0'], '', 'l0')['l0']
        temp = deconvolution(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Conv2DTranspose')
        # Test 2
        net['l1']['params']['weight_filler'] = 'xavier'
        net['l1']['params']['bias_filler'] = 'xavier'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = deconvolution(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[2].__class__.__name__, 'Conv2DTranspose')


class UpsampleExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Input2'], 'l2': net['Input4'], 'l3': net['Upsample']}
        # Conv 1D
        net['l1']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l1']
        net['l3']['params']['layer_type'] = '1D'
        inp = data(net['l1'], '', 'l1')['l1']
        temp = upsample(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[1].__class__.__name__, 'UpSampling1D')
        # Conv 2D
        net['l0']['connection']['output'].append('l0')
        net['l3']['connection']['input'] = ['l0']
        net['l3']['params']['layer_type'] = '2D'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = upsample(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[1].__class__.__name__, 'UpSampling2D')
        # Conv 3D
        net['l2']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l2']
        net['l3']['params']['layer_type'] = '3D'
        inp = data(net['l2'], '', 'l2')['l2']
        temp = upsample(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[1].__class__.__name__, 'UpSampling3D')


class PoolingExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Input2'], 'l2': net['Input4'], 'l3': net['Pooling']}
        # Pool 1D
        net['l1']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l1']
        net['l3']['params']['layer_type'] = '1D'
        net['l3']['shape']['input'] = net['l1']['shape']['output']
        net['l3']['shape']['output'] = [12, 12]
        inp = data(net['l1'], '', 'l1')['l1']
        temp = pooling(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[2].__class__.__name__, 'MaxPooling1D')
        # Pool 2D
        net['l0']['connection']['output'].append('l0')
        net['l3']['connection']['input'] = ['l0']
        net['l3']['params']['layer_type'] = '2D'
        net['l3']['shape']['input'] = net['l0']['shape']['output']
        net['l3']['shape']['output'] = [3, 226, 226]
        inp = data(net['l0'], '', 'l0')['l0']
        temp = pooling(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[2].__class__.__name__, 'MaxPooling2D')
        # Pool 3D
        net['l2']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l2']
        net['l3']['params']['layer_type'] = '3D'
        net['l3']['shape']['input'] = net['l2']['shape']['output']
        net['l3']['shape']['output'] = [3, 226, 226, 18]
        inp = data(net['l2'], '', 'l2')['l2']
        temp = pooling(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[2].__class__.__name__, 'MaxPooling3D')


# ********** Locally-connected Layers **********
class LocallyConnectedExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Input2'], 'l3': net['LocallyConnected']}
        # LocallyConnected 1D
        net['l1']['connection']['output'].append('l3')
        net['l3']['connection']['input'] = ['l1']
        net['l3']['params']['layer_type'] = '1D'
        inp = data(net['l1'], '', 'l1')['l1']
        temp = locally_connected(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[1].__class__.__name__, 'LocallyConnected1D')
        # LocallyConnected 2D
        net['l0']['connection']['output'].append('l0')
        net['l0']['shape']['output'] = [3, 10, 10]
        net['l3']['connection']['input'] = ['l0']
        net['l3']['params']['layer_type'] = '2D'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = locally_connected(net['l3'], [inp], 'l3')
        model = Model(inp, temp['l3'])
        self.assertEqual(model.layers[1].__class__.__name__, 'LocallyConnected2D')


# ********** Recurrent Layers Test **********
class RNNExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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

    def test_keras_export(self):
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


class GRUExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input2'], 'l1': net['GRU']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = recurrent(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'GRU')


# ********** Embed Layer Test *********
class EmbedExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input3'], 'l1': net['Embed']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        inp = data(net['l0'], '', 'l0')['l0']
        temp = embed(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Embedding')
        # Test 2
        net['l1']['params']['input_length'] = None
        net['l1']['params']['weight_filler'] = 'VarianceScaling'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = embed(net['l1'], [inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Embedding')


# ********** Merge Layers Test **********
class EltwiseExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['Eltwise']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        inp = data(net['l0'], '', 'l0')['l0']
        temp = eltwise(net['l1'], [inp, inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Multiply')
        # Test 2
        net['l1']['params']['layer_type'] = 'Sum'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = eltwise(net['l1'], [inp, inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Add')
        # Test 3
        net['l1']['params']['layer_type'] = 'Average'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = eltwise(net['l1'], [inp, inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Average')
        # Test 4
        net['l1']['params']['layer_type'] = 'Dot'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = eltwise(net['l1'], [inp, inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Dot')
        # Test 5
        net['l1']['params']['layer_type'] = 'Maximum'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = eltwise(net['l1'], [inp, inp], 'l1')
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'Maximum')


class ConcatExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
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


# ********** Noise Layers Test **********
class GaussianNoiseExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['GaussianNoise']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = gaussian_noise(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'GaussianNoise')


class GaussianDropoutExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['GaussianDropout']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = gaussian_dropout(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'GaussianDropout')


class AlphaDropoutExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['AlphaDropout']}
        net['l0']['connection']['output'].append('l1')
        inp = data(net['l0'], '', 'l0')['l0']
        net = alpha_dropout(net['l1'], [inp], 'l1')
        model = Model(inp, net['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'AlphaDropout')


# ********** Normalisation Layers Test **********
class BatchNormExportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_keras_export(self):
        tests = open(os.path.join(settings.BASE_DIR, 'tests', 'unit', 'keras_app',
                                  'keras_export_test.json'), 'r')
        response = json.load(tests)
        tests.close()
        net = yaml.safe_load(json.dumps(response['net']))
        net = {'l0': net['Input'], 'l1': net['BatchNorm'], 'l2': net['Scale']}
        net['l0']['connection']['output'].append('l1')
        # Test 1
        inp = data(net['l0'], '', 'l0')['l0']
        temp = batch_norm(net['l1'], [inp], 'l1', 'l2', net['l2'])
        model = Model(inp, temp['l2'])
        self.assertEqual(model.layers[1].__class__.__name__, 'BatchNormalization')
        # Test 2
        net['l2']['params']['filler'] = 'VarianceScaling'
        net['l2']['params']['bias_filler'] = 'VarianceScaling'
        inp = data(net['l0'], '', 'l0')['l0']
        temp = batch_norm(net['l1'], [inp], 'l1', 'l2', net['l2'])
        model = Model(inp, temp['l2'])
        self.assertEqual(model.layers[1].__class__.__name__, 'BatchNormalization')
        # Test 3
        inp = data(net['l0'], '', 'l0')['l0']
        temp = batch_norm(net['l1'], [inp], 'l1', 'l0', net['l0'])
        model = Model(inp, temp['l1'])
        self.assertEqual(model.layers[1].__class__.__name__, 'BatchNormalization')
