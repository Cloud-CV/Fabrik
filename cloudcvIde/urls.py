from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^export_caffe$', views.exportToCaffe, name='exportToCaffe'),
    url(r'^export_tensorflow$', views.exportToTensorflow, name='exportToTensorflow'),
    url(r'^import$', views.importModel, name='import'),
]
