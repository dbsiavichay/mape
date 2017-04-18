# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
	birthday = models.DateField(blank=True, null=True)
	cellphone = models.CharField(max_length=32, blank=True, null=True)
	avatar = models.ImageField(upload_to='social/avatares/', blank=True, null=True)
	user = models.OneToOneField(User)
