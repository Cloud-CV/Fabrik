from django.conf.urls import url
from views.import_prototxt import import_prototxt
from views.export_prototxt import export_to_caffe
from views.DB import save_to_db
from views.DB import load_from_db

urlpatterns = [
    url(r'^export$', export_to_caffe, name='caffe-export'),
    url(r'^import$', import_prototxt, name='caffe-import'),
    url(r'^save$', save_to_db, name='saveDB'),
    url(r'^load*', load_from_db, name='loadDB')
]
