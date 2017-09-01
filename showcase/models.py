# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models

from django.contrib.contenttypes.models import ContentType

from django.contrib.gis.geos import Point

class Category(models.Model):
	name = models.CharField(max_length=64, unique=True)

	def __unicode__(self):
		return self.name

class Locality(models.Model):
	name = models.CharField(max_length=45, verbose_name='nombre')
	description = models.TextField(blank=True, null=True, verbose_name='descripción')
	front_image = models.ImageField(upload_to='showcase/localities/', blank=True, null=True)
	profile_image = models.ImageField(upload_to='showcase/localities/', blank=True, null=True)	
	latitude = models.FloatField(verbose_name='latitud')
	longitude = models.FloatField(verbose_name='longitud')
	point = models.PointField(null=True, blank=True)
	###Por defecto TRUE cuando ya es comercial
	is_public = models.BooleanField(default=False, verbose_name='visible a todos?')
	###
	is_commercial = models.BooleanField(default=False, verbose_name='es comercial?')
	verified = models.BooleanField(default=False,)	
	date_joined = models.DateTimeField(auto_now_add=True)	
	owner = models.ForeignKey('social.Profile')	
	categories = models.ManyToManyField(Category, verbose_name='categorias')

	def __unicode__(self):
		return self.name

	def comments(self):
		from social.models import Comment
		contenttype = ContentType.objects.get_for_model(Locality)
		comments = Comment.objects.filter(contenttype = contenttype, object_id=self.id)
		return comments

	def subscribers_count(self):
		from social.models import Subscriber
		contenttype = ContentType.objects.get_for_model(Locality)
		count = Subscriber.objects.filter(contenttype = contenttype, object_id=self.id).count()
		return count

class Commercial(models.Model):
	ruc = models.CharField(max_length=13)
	telephone = models.CharField(max_length=30, verbose_name='telefono')
	address = models.CharField(max_length=100, verbose_name='Dirección')
	webpage = models.URLField(verbose_name='página web')
	locality = models.OneToOneField(Locality, on_delete=models.CASCADE)		
	
	def __unicode__(self):
		return self.locality.name

class Offer(models.Model):
	PRODUCT = 1
	SERVICE = 2

	KIND_CHOICES = (
		(PRODUCT, 'Producto'),
		(SERVICE, 'Servicio')
	)

	name = models.CharField(max_length=64, verbose_name='nombre')
	description = models.TextField(null=True, blank=True, verbose_name='descripción')
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='precio')	
	image = models.ImageField(upload_to='showcase/offers/', null=True, blank=True)
	kind = models.PositiveSmallIntegerField(choices = KIND_CHOICES, verbose_name='tipo')	
	commercial = models.ForeignKey(Commercial)

	def __unicode__(self):
		return unicode(self.name)

	def get_kind(self):
		return 'producto' if self.kind == Offer.PRODUCT else 'servicio'



##EVENTOS
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
		default=0,
		verbose_name = 'precio de entrada'
	)
	is_public = models.BooleanField(default=False)
	link = models.CharField(max_length=128, blank=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	locality = models.ForeignKey(Locality, blank=True, null=True)		
	guests = models.ManyToManyField('social.Profile', through='Guest', blank=True)

	def __unicode__(self):
		return self.name

	def invited_count(self):
		return self.guests.all().count() - 1

	def is_free(self):
		return False if self.cover > 0 else True

	def get_organizers(self):
		return self.guests.filter(guest__is_organizer=True)

	def get_information(self):
		invited = self.guests.all()
		attend = self.guests.filter(guest__status=Guest.ATTEND)
		liked = self.guests.filter(guest__status=Guest.LIKE)		

		return '%s invitados * %s asistirán * %s les gusta' % (len(invited) - 1, len(attend), len(liked))

	def comments(self):
		from social.models import Comment
		contenttype = ContentType.objects.get_for_model(Event)
		comments = Comment.objects.filter(contenttype = contenttype, object_id=self.id)
		return comments


class Guest(models.Model):
	INVITED = 1
	ATTEND = 2
	LIKE = 3
	MAYBE_ATTEND = 4
	NOT_ATTEND = 5


	STATE_CHOICES = (
		(INVITED, 'Invitado'),
		(ATTEND, 'Asistirá'),
		(LIKE, 'Me gusta'),
		(MAYBE_ATTEND, 'Talvez asista'),
		(NOT_ATTEND, 'No asistirá')
	)

	class Meta:
		unique_together = (('profile', 'event'),)
	
	profile = models.ForeignKey('social.Profile', on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	is_creator = models.BooleanField(default=False)
	is_organizer = models.BooleanField(default=False)
	status = models.PositiveSmallIntegerField(default = INVITED, choices = STATE_CHOICES) 
	date = models.DateTimeField(auto_now_add=True)	

	def attend(self, action=True):
		self.state = 2 if action else 3		