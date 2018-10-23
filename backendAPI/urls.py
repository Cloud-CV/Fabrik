from django.conf.urls import url
from views import check_login

urlpatterns = [
    url(r'^checkLogin$', check_login)
]
