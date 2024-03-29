# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models

from notifications.mixins import NotificationMixin
from django.contrib.gis.geos import Point

from shower.managers import ShowerManager

class Category(models.Model):
	name = models.CharField(max_length=64, unique=True)

	def __unicode__(self):
		return unicode(self.name)

class Locality(models.Model):
	class Meta:
		verbose_name = 'localidad'
		verbose_name_plural = 'localidades'

	name = models.CharField(max_length=45, verbose_name='nombre', unique=True)
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
	owner = models.ForeignKey('social.Profile', on_delete=models.CASCADE)	
	categories = models.ManyToManyField(Category, verbose_name='categorias')
	objects = ShowerManager()

	def __unicode__(self):
		return unicode(self.name)

	def get_hash_name(self):
		return self.name.replace(" ", "_")

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('locality_detail', args=[str(self.id)])

class Commercial(models.Model):
	ruc = models.CharField(max_length=13)
	telephone = models.CharField(max_length=30, verbose_name='telefono')
	address = models.CharField(max_length=100, verbose_name='Dirección')
	webpage = models.URLField(verbose_name='página web', blank=True, null=True)
	locality = models.OneToOneField(Locality, on_delete=models.CASCADE)		
	
	def __unicode__(self):
		return self.locality.name

class Offer(models.Model):
	class Meta:
		verbose_name='oferta'

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
	commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE)
	objects = ShowerManager()

	def __unicode__(self):
		return unicode(self.name)

	def get_kind(self):
		return 'producto' if self.kind == Offer.PRODUCT else 'servicio'



##EVENTOS
class Event(models.Model):
	class Meta:
		verbose_name = 'evento'
		verbose_name_plural = 'eventos'

	STATUS_CHOICES = (
		(1, 'Activo'),
		(2, 'Completado'),
		(3, 'Cancelado'),		
	)

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
	locality = models.ForeignKey(Locality, blank=True, null=True, on_delete=models.CASCADE)		
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
	guests = models.ManyToManyField('social.Profile', through='Guest', blank=True)
	objects = ShowerManager()


	def __unicode__(self):
		return unicode(self.name)

	def invited_count(self):
		return self.guests.all().count() - 1

	def is_free(self):
		return False if self.cover > 0 else True

	def owner(self):
		return self.guests.get(guest__is_owner=True)

	def get_information(self):
		from django.contrib.contenttypes.models import ContentType
		from subscribers.models import Subscriber
		invited = self.guests.all()
		attend = self.guests.filter(guest__status=Guest.ATTEND)
		
		ctype = ContentType.objects.get_for_model(self)
		likers = Subscriber.objects.filter(contenttype = ctype, object_id=self.id).count()
	    

		return '%s | %s invitados * %s asistirán * %s les gusta' % (
			'Público' if self.is_public else 'Privado',
			len(invited) - 1, len(attend), likers)

	def get_is_comming(self):
		from datetime import datetime
		if self.status == 3: return 'Cancelado'
		now = datetime.now().date()
		delta = self.start.date() - now
		days = delta.days
		if days < 0 and self.status == 1:			
			self.status = 2
			self.save()
		if days >= 0 and days < 7:
			return 'Esta semana'
		elif days > 7:
			return 'Por venir'
		else:
			return 'Completado'

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('event_detail', args=[str(self.id)])

class Guest(NotificationMixin, models.Model):
	INVITED = 1
	ATTEND = 2	
	MAYBE_ATTEND = 3
	NOT_ATTEND = 4
	SPONSOR_REQUEST = 5

	STATE_CHOICES = (
		(INVITED, 'Invitado'),
		(ATTEND, 'Asistirá'),		
		(MAYBE_ATTEND, 'Talvez asista'),
		(NOT_ATTEND, 'No asistirá')
	)

	class Meta:
		unique_together = (('profile', 'event'),)
	
	profile = models.ForeignKey('social.Profile', on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	is_owner = models.BooleanField(default=False)
	is_sponsor = models.BooleanField(default=False)
	status = models.PositiveSmallIntegerField(default = INVITED, choices = STATE_CHOICES) 
	date = models.DateTimeField(auto_now_add=True)	

	def attend(self, action=True):
		self.state = 2 if action else 3	

