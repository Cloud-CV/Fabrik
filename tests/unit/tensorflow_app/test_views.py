import json
import os
import unittest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client
from ide.utils.shapes import get_shapes


class UploadTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        sample_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'GoogleNet.pbtxt'),
                           'r')
        response = self.client.post(reverse('tf-import'), {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class ConvLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'Conv3DCheck.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class DeconvLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'denoiseAutoEncoder.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class PoolLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'Pool3DCheck.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class RepeatLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'Conv2DRepeat.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class StackLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'FCStack.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class DepthwiseConvLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'DepthwiseConv.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class BatchNormLayerTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'BatchNorm.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')


class LRNImportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_export(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/keras',
                                       'AlexNet.json'), 'r')
        response = self.client.post(reverse('keras-import'), {'file': model_file})
        response = json.loads(response.content)
        net = get_shapes(response['net'])
        response = self.client.post(reverse('tf-export'), {'net': json.dumps(net),
                                                           'net_name': ''})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')

    def test_custom_lrn_tf_import(self):
        model_file = open(os.path.join(settings.BASE_DIR, 'example/tensorflow', 'LRN.pbtxt'),
                          'r')
        response = self.client.post(reverse('tf-import'), {'file': model_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
