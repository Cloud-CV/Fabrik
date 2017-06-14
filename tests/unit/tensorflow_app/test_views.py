import json
import os
import unittest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client


class UploadTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tf_import(self):
        sample_file = open(os.path.join(settings.BASE_DIR, 'example', 'GoogleNet.pbtxt'), 'r')
        response = self.client.post(reverse('tf-import'), {'file': sample_file})
        response = json.loads(response.content)
        self.assertEqual(response['result'], 'success')
