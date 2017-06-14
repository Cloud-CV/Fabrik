from django.conf.urls import url
from views.import_graphdef import importGraphDef
from views.export_graphdef import exportToTensorflow

urlpatterns = [
    url(r'^export$', exportToTensorflow, name='tf-export'),
    url(r'^import$', importGraphDef, name='tf-import'),
]
