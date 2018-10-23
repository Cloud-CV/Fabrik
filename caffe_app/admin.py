# Register your models here.
from django.contrib import admin
from .models import SharedWith, Network

admin.site.register(SharedWith)
admin.site.register(Network)
