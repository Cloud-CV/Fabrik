
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
	url(r'^cloudcvide/', include('cloudcvIde.urls')),
    url(r'^admin/', admin.site.urls),
]

