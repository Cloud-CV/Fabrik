from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from django.contrib.postgres.fields import JSONField


class Network(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, blank=True, null=True)
    public_sharing = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id


class NetworkVersion(models.Model):
    network = models.ForeignKey(Network)
    network_def = JSONField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.id


class NetworkUpdates(models.Model):
    network_version = models.ForeignKey(NetworkVersion)
    updated_data = JSONField()
    tag = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag


class SharedWith(models.Model):
    ACCESS_PRIVILEGE = (
        ('E', 'Can Edit'),
        ('V', 'Can View'),
        ('C', 'Can Comment')
    )
    network = models.ForeignKey(Network)
    user = models.ForeignKey(User)
    access_privilege = models.CharField(max_length=1, choices=ACCESS_PRIVILEGE)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username
