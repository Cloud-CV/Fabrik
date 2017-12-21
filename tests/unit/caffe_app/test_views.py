import caffe
import json
import os
import unittest

from caffe import layers as L, params as P, to_proto
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client


class ImportPrototxtTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        sample_file = open(os.path.join(settings.BASE_DIR,
                                        'example/caffe',
                                        'GoogleNet.prototxt'), 'r')
        # Test 1
        response = self.client.post(reverse('caffe-import'),
                                    {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
        # Test 2
        sample_file = open(os.path.join(settings.BASE_DIR,
                                        'example/keras',
                                        'vgg16.json'), 'r')
        response = self.client.post(reverse('caffe-import'),
                                    {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'error')
        self.assertEqual(response['error'], 'Invalid Prototxt')

    def test_caffe_import_by_sample_id(self):
        response = self.client.post(reverse('caffe-import'),
                                    {'sample_id': 'GoogleNet'})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
        response = self.client.post(reverse('caffe-import'),
                                    {'sample_id': 'vgg15'})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'error')
        self.assertEqual(response['error'], 'No Prototxt model file found')


class ExportPrototxtTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_export(self):
        data = L.Input(shape={'dim': [10, 3, 224, 224]})
        top = L.Convolution(data, kernel_size=3, pad=1, stride=1, num_output=128, dilation=1,
                            weight_filler={'type': 'xavier'}, bias_filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        response['net']['l0']['params']['caffe'] = True
        response['net']['l1']['params']['caffe'] = True
        response = self.client.post(reverse('caffe-export'), {'net': json.dumps(response['net']),
                                                              'net_name': ''})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class ExportPrototxtFailTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_export(self):
        data = L.Input(shape={'dim': [10, 3, 16, 224, 224]})
        top = L.Convolution(data, kernel_size=3, pad=1, stride=1, num_output=128, dilation=1,
                            weight_filler={'type': 'xavier'}, bias_filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        response['net']['l0']['params']['caffe'] = True
        response['net']['l1']['params']['layer_type'] = '3D'
        response['net']['l1']['params']['caffe'] = False
        response = self.client.post(reverse('caffe-export'), {'net': json.dumps(response['net']),
                                                              'net_name': ''})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'error')


# ********** Data Layers Test **********
class ImageDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        data, label = L.ImageData(source='/dummy/source/', batch_size=32, ntop=2, rand_skip=0,
                                  shuffle=False, new_height=256, new_width=256, is_color=False,
                                  root_folder='/dummy/folder/',
                                  transform_param=dict(crop_size=227, mean_value=[104, 117, 123],
                                                       mirror=True, force_color=False,
                                                       force_gray=False))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 13)
        self.assertEqual(response['result'], 'success')
        # Test 2
        data, label = L.ImageData(source='/dummy/source/', batch_size=32, ntop=2, rand_skip=0,
                                  shuffle=False, new_height=256, new_width=256, is_color=False,
                                  root_folder='/dummy/folder/', include=dict(phase=caffe.TRAIN),
                                  transform_param=dict(crop_size=227, mean_file='/path/to/file',
                                                       mirror=True, force_color=False,
                                                       force_gray=False))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 13)
        self.assertEqual(response['result'], 'success')


class DataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        data, label = L.Data(source='/dummy/source/', backend=P.Data.LMDB, batch_size=32, ntop=2,
                             rand_skip=0, prefetch=10,
                             transform_param=dict(crop_size=227, mean_value=[104, 117, 123],
                                                  mirror=True, force_color=False,
                                                  force_gray=False))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 10)
        self.assertEqual(response['result'], 'success')
        # Test 2
        data, label = L.Data(source='/dummy/source/', backend=P.Data.LEVELDB, batch_size=32, ntop=2,
                             rand_skip=0, prefetch=10,
                             transform_param=dict(crop_size=227, mean_value=[104, 117, 123],
                                                  mirror=True, force_color=False,
                                                  force_gray=False))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 10)
        self.assertEqual(response['result'], 'success')


class HDF5DataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        data, label = L.HDF5Data(source='/dummy/source/', batch_size=32, ntop=2, shuffle=False)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class HDF5OutputLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.HDF5Output(file_name='/dummy/filename')
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class InputLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        data = L.Input(shape={'dim': [10, 3, 224, 224]})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class WindowDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        data, label = L.WindowData(source='/dummy/source/', batch_size=32, ntop=2,
                                   fg_threshold=0.5, bg_threshold=0.5, fg_fraction=0.25,
                                   context_pad=0, crop_mode='warp', cache_images=False,
                                   root_folder='/dummy/folder/',
                                   transform_param=dict(crop_size=227, mean_value=[104, 117, 123],
                                                        mirror=True, force_color=False,
                                                        force_gray=False))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 14)
        self.assertEqual(response['result'], 'success')


class MemoryDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        data, label = L.MemoryData(batch_size=32, ntop=2, channels=3, height=224, width=224)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data, label)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 4)
        self.assertEqual(response['result'], 'success')


class DummyDataLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        data = L.DummyData(shape={'dim': [10, 3, 224, 224]},
                           data_filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(data)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


# ********** Vision Layers Test **********
class ConvolutionLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        top = L.Convolution(kernel_size=3, pad=1, stride=1, num_output=128,
                            weight_filler={'type': 'xavier'}, bias_filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 6)
        self.assertEqual(response['result'], 'success')
        # Test 2
        top = L.Convolution(kernel_w=3, kernel_h=3, pad_w=1, pad_h=1, stride=1, num_output=128,
                            weight_filler={'type': 'xavier'}, bias_filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 6)
        self.assertEqual(response['result'], 'success')


class PoolingLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        top = L.Pooling(kernel_size=2, pad=0, stride=2, pool=1)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 4)
        self.assertEqual(response['result'], 'success')
        # Test 2
        top = L.Pooling(kernel_size=2, pad=0, stride=2, pool=2)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 4)
        self.assertEqual(response['result'], 'success')


class SPPLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.SPP(pyramid_height=2, pool=1)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 2)
        self.assertEqual(response['result'], 'success')


class CropLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Crop(axis=2, offset=2)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 2)
        self.assertEqual(response['result'], 'success')


class DeconvolutionLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        top = L.Deconvolution(convolution_param=dict(kernel_size=3, pad=1, stride=1, num_output=128,
                              weight_filler={'type': 'xavier'}, bias_filler={'type': 'constant'}))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 6)
        self.assertEqual(response['result'], 'success')
        # Test 2
        top = L.Deconvolution(convolution_param=dict(kernel_w=3, kernel_h=3, pad_w=1, pad_h=1, stride=1,
                              num_output=128, dilation=1, weight_filler={'type': 'xavier'},
                              bias_filler={'type': 'constant'}))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 6)
        self.assertEqual(response['result'], 'success')


# ********** Recurrent Layers Test **********
class RecurrentLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Recurrent(recurrent_param=dict(num_output=128, debug_info=False,
                          expose_hidden=False, weight_filler={'type': 'xavier'},
                          bias_filler={'type': 'constant'}))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 5)
        self.assertEqual(response['result'], 'success')


class RNNLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.RNN(recurrent_param=dict(num_output=128, debug_info=False,
                    expose_hidden=False, weight_filler={'type': 'xavier'},
                    bias_filler={'type': 'constant'}))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 5)
        self.assertEqual(response['result'], 'success')


class LSTMLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.LSTM(recurrent_param=dict(num_output=128, debug_info=False,
                     expose_hidden=False, weight_filler={'type': 'xavier'},
                     bias_filler={'type': 'constant'}))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 5)
        self.assertEqual(response['result'], 'success')


# ********** Common Layers Test **********
class InnerProductLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.InnerProduct(num_output=128, weight_filler={'type': 'xavier'},
                             bias_filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class DropoutLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Dropout()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class EmbedLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Embed(num_output=128, input_dim=2, bias_term=False,
                      weight_filler={'type': 'xavier'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 4)
        self.assertEqual(response['result'], 'success')


# ********** Normalisation Layers Test **********
class LRNLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.LRN(local_size=5, alpha=1, beta=0.75, k=1, norm_region=1, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 5)
        self.assertEqual(response['result'], 'success')


class MVNLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.MVN(normalize_variance=True, eps=1e-9, across_channels=False, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class BatchNormLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.BatchNorm(use_global_stats=True, moving_average_fraction=0.999, eps=1e-5, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


# ********** Activation / Neuron Layers Test **********
class ReLULayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.ReLU(negative_slope=0, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class PReLULayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.PReLU(channel_shared=False, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class ELULayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.ELU(alpha=1, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class SigmoidLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Sigmoid(in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class TanHLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.TanH(in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class AbsValLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.AbsVal(in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class PowerLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Power(power=1.0, scale=1.0, shift=0.0, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class ExpLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Exp(base=-1.0, scale=1.0, shift=0.0, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class LogLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Log(base=-1.0, scale=1.0, shift=0.0, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class BNLLLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.BNLL(in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class ThresholdLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Threshold(threshold=1.0, in_place=True)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class BiasLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Bias(axis=1, num_axes=1, filler={'type': 'constant'})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class ScaleLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Scale(bias_term=False)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


# ********** Utility Layers Test **********
class FlattenLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Flatten(axis=1, end_axis=-1)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 2)
        self.assertEqual(response['result'], 'success')


class ReshapeLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Reshape(shape={'dim': [2, -1]})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class BatchReindexLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.BatchReindex()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class SplitLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Split()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class ConcatLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Concat()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class SliceLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Slice(axis=1, slice_dim=1, slice_point=[1, 2])
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class EltwiseLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        top = L.Eltwise(operation=2)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class FilterLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Filter()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


# This layer is currently not supported as there is no bottom blob
'''class ParameterLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Parameter(shape={'dim': [10, 3, 224, 224]})
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')
'''


class ReductionLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        top = L.Reduction(operation=1, axis=0, coeff=1.0)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')
        # Test 2
        top = L.Reduction(operation=2, axis=0, coeff=1.0)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')
        # Test 3
        top = L.Reduction(operation=3, axis=0, coeff=1.0)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')
        # Test 4
        top = L.Reduction(operation=4, axis=0, coeff=1.0)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')
        # Test 5
        top = L.Reduction(axis=0, coeff=1.0)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['net']['l0']['params']['operation'], 'SUM')
        self.assertEqual(response['result'], 'success')


class SilenceLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Silence()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class ArgMaxLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.ArgMax(out_max_val=False, top_k=1, axis=0)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 3)
        self.assertEqual(response['result'], 'success')


class SoftmaxLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.Softmax()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


# ********** Loss Layers Test **********
class MultinomialLogisticLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.MultinomialLogisticLoss()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class InfogainLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.InfogainLoss(source='/dummy/source/', axis=1)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 2)
        self.assertEqual(response['result'], 'success')


class SoftmaxWithLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.SoftmaxWithLoss(softmax_param=dict(axis=1))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class EuclideanLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.EuclideanLoss()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class HingeLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.HingeLoss(norm=2)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 1)
        self.assertEqual(response['result'], 'success')


class SigmoidCrossEntropyLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.SigmoidCrossEntropyLoss()
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertEqual(response['result'], 'success')


class AccuracyLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        data = L.Input(shape={'dim': [10, 100]})
        top = L.Accuracy(data, axis=1, top_k=1, include=dict(phase=caffe.TEST))
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l1']['params']), 2)
        self.assertEqual(response['result'], 'success')


class ContrastiveLossLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        top = L.ContrastiveLoss(margin=1.0, legacy_version=False)
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 2)
        self.assertEqual(response['result'], 'success')


# ********** Python Layer Test **********
class PythonLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_caffe_import(self):
        # Test 1
        data = L.Input(shape={'dim': [10, 3, 224, 224]})
        top = L.Python(data, module='pyloss', layer='EuclideanLossLayer', loss_weight=1, name='eucLoss')
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l1']['params']), 4)
        self.assertEqual(response['result'], 'success')
        # Test 2
        top = L.Python(module='pascal_multilabel_datalayers', layer='PascalMultilabelDataLayerSync',
                       param_str="{\'pascal_root\': \'../data/pascal/VOC2007\', \'im_shape\': [227, 227], \
                        \'split\': \'train\', \'batch_size\': 128}")
        with open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'w') as f:
            f.write(str(to_proto(top)))
        sample_file = open(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'), 'r')
        response = self.client.post(reverse('caffe-import'), {'file': sample_file})
        response = json.loads(response.content)
        os.remove(os.path.join(settings.BASE_DIR, 'media', 'test.prototxt'))
        self.assertGreaterEqual(len(response['net']['l0']['params']), 6)
        self.assertEqual(response['result'], 'success')
