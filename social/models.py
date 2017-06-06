# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from PIL import Image

class Profile(models.Model):
	charter = models.CharField(max_length=10, blank=True, null=True, verbose_name='cédula')
	birthday = models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')
	cellphone = models.CharField(max_length=32, blank=True, null=True, verbose_name='número de celular')
	avatar = models.ImageField(upload_to='social/avatares/', blank=True, null=True,)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)

	def get_friends_count(self):
		return len(self.friends.filter(relationship__status=2))

	def get_relationship(self, profile, status):
		f = Friendship.objects.filter(from_profile=self, to_profile=profile, status=status)
		if len(f) > 0:
			return True

		f = Friendship.objects.filter(from_profile=profile, to_profile=self, status=status)
		if len(f) > 0:
			return True
		else:
			return False		

	def send_request(self, friend):
		self.friends.add(friend)



	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		if self.avatar:
			process_image(self.avatar, 500)

class Friendship(models.Model):
	STATE_CHOICES = (
		(1, 'Solicitud'),
		(2, 'Amistad'),		
	)

	from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='relationship')
	to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_profile')
	status = models.PositiveSmallIntegerField(default=1, choices=STATE_CHOICES)
	date_joined = models.DateTimeField(auto_now=True)

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
