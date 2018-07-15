from django.conf.urls import url
from views.import_prototxt import import_prototxt
from views.export_prototxt import export_to_caffe

urlpatterns = [
    url(r'^export$', export_to_caffe, name='caffe-export'),
    url(r'^import$', import_prototxt, name='caffe-import'),
]
