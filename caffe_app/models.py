from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from django.contrib.postgres.fields import JSONField


class ModelExport(models.Model):
    name = models.CharField(max_length=100)
    id = models.CharField(max_length=20, primary_key=True)
    network = JSONField()
    createdOn = models.DateField(auto_now_add=True)
    updatedOn = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.id
