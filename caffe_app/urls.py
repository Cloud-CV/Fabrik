from django.conf.urls import url
from views.import_prototxt import *
from views.export_prototxt import *

urlpatterns = [
    url(r'^export$', exportToCaffe),
    url(r'^import$', importPrototxt),
]
