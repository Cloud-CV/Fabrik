from django.conf.urls import url
from views.views import *
from views.importPrototxt import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^export_caffe$', exportToCaffe, name='exportToCaffe'),
    url(r'^export_tensorflow$', exportToTensorflow, name='exportToTensorflow'),
    url(r'^import$', importPrototxt, name='import'),
]
