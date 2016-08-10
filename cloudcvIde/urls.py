from django.conf.urls import url
from views.views import *
from views.importPrototxt import *
from views.importGraphDef import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^export_caffe$', exportToCaffe, name='exportToCaffe'),
    url(r'^export_tensorflow$', exportToTensorflow, name='exportToTensorflow'),
    url(r'^import_caffe$', importPrototxt, name='importFromCaffe'),
    url(r'^import_tensorflow$', importGraphDef, name='importFromTensorflow'),
]
