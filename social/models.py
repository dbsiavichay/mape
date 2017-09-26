# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.contrib.contenttypes.models import ContentType

from .managers import FriendshipManager
from shower.managers import ShowerManager
from notifications.mixins import NotificationMixin

from PIL import Image

class Profile(models.Model):
	class Meta:
		verbose_name = 'persona'

	charter = models.CharField(max_length=10, blank=True, null=True, verbose_name='cédula')
	birthday = models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')
	cellphone = models.CharField(max_length=32, blank=True, null=True, verbose_name='número de celular')
	avatar = models.ImageField(upload_to='social/avatares/', blank=True, null=True,)	
	is_complete = models.BooleanField(default=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	objects = ShowerManager()

	def __unicode__(self):
		return self.user

	def get_full_name(self):
		return self.user.get_full_name()
		
	def get_profiles(self, status):
		profiles = []

		friendships = Friendship.objects.filter(
			models.Q(from_profile=self) |
			models.Q(to_profile=self)
		).filter(status=status)

		for friendship in friendships:
			profile = friendship.from_profile if friendship.to_profile == self else friendship.to_profile
			profiles.append(profile)

		return profiles		

	def friends(self):				
		friends = self.get_profiles(Friendship.FRIENDSHIP_FRIEND)
		return friends

	def blocked_friends(self):					
		blocked = self.get_profiles(Friendship.FRIENDSHIP_BLOCKED)
		return blocked

	def requests(self):
		profiles = []

		friendships = Friendship.objects.filter(
			to_profile=self,
			status=Friendship.FRIENDSHIP_REQUEST
		)

		for friendship in friendships:			
			profiles.append(friendship.from_profile)

		return profiles

	def sent_requests(self):
		profiles = []

		friendships = Friendship.objects.filter(
			from_profile=self,
			status=Friendship.FRIENDSHIP_REQUEST
		)

		for friendship in friendships:			
			profiles.append(friendship.to_profile)

		return profiles

	def commercial(self):
		from showcase.models import Locality
		try:
			locality = Locality.objects.get(owner=self, is_commercial=True)
			return locality.commercial
		except Locality.DoesNotExist:
			return None

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('profile_detail', args=[str(self.user.username)])

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		if self.avatar:
			process_image(self.avatar, 500)

class Friendship(NotificationMixin, models.Model):
	FRIENDSHIP_REQUEST = 1
	FRIENDSHIP_FRIEND = 2
	FRIENDSHIP_BLOCKED = 3

	STATE_CHOICES = (
		(FRIENDSHIP_REQUEST, 'Solicitud'),
		(FRIENDSHIP_FRIEND, 'Amistad'),		
		(FRIENDSHIP_BLOCKED, 'Bloqueado'),		
	)

	class Meta:
		unique_together = ('from_profile', 'to_profile')

	from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='relationship')
	to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_profile')
	status = models.PositiveSmallIntegerField(default=1, choices=STATE_CHOICES)
	date_joined = models.DateTimeField(auto_now=True)

	objects = FriendshipManager()		

def process_image(image_field, size):
	image = Image.open(image_field)
	width, height = image.size
	box = (0,0,width, height)

	if width > height:
		value = (width - height) / 2
		box = (value, 0, width - value, height)
	else:
		value = (height - width) / 2
		box = (0, value, width, height - value)

	cut_image = image.crop(box)

	new_size = cut_image.width

	if new_size > size:
		cut_image = cut_image.resize((size, size), Image.ANTIALIAS)

	cut_image.save(image_field.path)
