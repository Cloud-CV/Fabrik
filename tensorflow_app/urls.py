from django.conf.urls import url
from views.import_graphdef import *
from views.export_graphdef import *

urlpatterns = [
    url(r'^export$', exportToTensorflow),
    url(r'^import$', importGraphDef),
]
