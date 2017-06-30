from django.conf.urls import url
from views.import_json import importJson
from views.export_json import exportJson

urlpatterns = [
    url(r'^import$', importJson, name='keras-import'),
    url(r'^export$', exportJson, name='keras-export')
]
