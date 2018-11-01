from django.conf.urls import url
from .views.import_graphdef import import_graph_def
from .views.export_graphdef import export_to_tensorflow

urlpatterns = [
    url(r'^export$', export_to_tensorflow, name='tf-export'),
    url(r'^import$', import_graph_def, name='tf-import'),
]
