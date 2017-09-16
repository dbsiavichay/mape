# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Subscriber(models.Model):
	object_id = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
	contenttype = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
	profile = models.ForeignKey('social.Profile', on_delete=models.CASCADE)