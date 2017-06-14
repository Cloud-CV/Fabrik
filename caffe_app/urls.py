from django.conf.urls import url
from views.import_prototxt import importPrototxt
from views.export_prototxt import exportToCaffe

urlpatterns = [
    url(r'^export$', exportToCaffe, name='caffe-export'),
    url(r'^import$', importPrototxt, name='caffe-import'),
]
