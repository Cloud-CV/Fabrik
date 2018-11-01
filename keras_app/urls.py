from django.conf.urls import url
from .views.import_json import import_json
from .views.export_json import export_json

urlpatterns = [
    url(r'^import$', import_json, name='keras-import'),
    url(r'^export$', export_json, name='keras-export')
]
