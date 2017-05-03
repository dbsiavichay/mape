# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
	name = models.CharField(max_length=64, verbose_name='nombre')
	description = models.TextField(blank=True, null=True, verbose_name='descripción')
	front_image = models.ImageField(
		upload_to='showcase/events/', 
		null=True, blank=True, 
		verbose_name = 'portada'
	)	 	
	latitude = models.FloatField()
	longitude = models.FloatField(default=0)
	when = models.DateTimeField(verbose_name='Inicio')
	ends = models.DateTimeField(blank=True, null=True)	
	cover = models.DecimalField(
		decimal_places=2, max_digits=8, 
		blank=True, null=True,
		verbose_name = 'precio de entrada'
	)
	is_public = models.BooleanField(default=False)
	link = models.CharField(max_length=128, blank=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=True)	
	published_by = models.ForeignKey(User)

	def __unicode__(self):
		return self.name
