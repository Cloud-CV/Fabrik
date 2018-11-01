from __future__ import unicode_literals

from django.apps import AppConfig

from . import startup


class KerasAppConfig(AppConfig):
    name = 'keras_app'

startup.run()
