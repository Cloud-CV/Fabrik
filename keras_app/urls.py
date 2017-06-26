from django.conf.urls import url
from views.import_json import importJson

urlpatterns = [
    url(r'^import$', importJson, name='keras-import')
]
