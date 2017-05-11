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
	start = models.DateTimeField()
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

class Category(models.Model):
	name = models.CharField(max_length=64, unique=True)

	def __unicode__(self):
		return unicode(self.name)

class Locality(models.Model):
	name = models.CharField(max_length=45)
	description = models.TextField(blank=True, null=True)
	front_image = models.ImageField(upload_to='showcase/localities/', blank=True, null=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	date_joined = models.DateField(auto_now_add=True)	
	categories = models.ManyToManyField(Category)
	subscribers = models.ManyToManyField(User, through='LocalitySubscriber')	

	def __unicode__(self):
		return self.name

class LocalitySubscriber(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
	is_owner = models.BooleanField(default=False)

class Commercial(models.Model):	
	ruc = models.CharField(max_length=13)
	locality = models.OneToOneField(Locality, on_delete=models.CASCADE)			
	
	def __unicode__(self):
		return self.locality.name

class Group(models.Model):
	KIND_CHOICES = (
		(1, 'Producto'),
		(2, 'Servicio')
	)

	name = models.CharField(max_length=64)
	kind = models.PositiveSmallIntegerField(choices = KIND_CHOICES)
	commercial = models.ForeignKey(Commercial)

	def __unicode__(self):
		return self.name

class Offer(models.Model):
	name = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0)	
	image = models.ImageField(upload_to='showcase/offers/', null=True, blank=True)
	group = models.ForeignKey(Group)

	def __unicode__(self):
		return unicode(self.name)





