# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from PIL import Image

class Profile(models.Model):
	charter = models.CharField(max_length=10, blank=True, null=True, verbose_name='cédula')
	birthday = models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')
	cellphone = models.CharField(max_length=32, blank=True, null=True, verbose_name='número de celular')
	avatar = models.ImageField(upload_to='social/avatares/', blank=True, null=True, verbose_name='imagen de perfil')
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		if self.avatar:
			process_image(self.avatar, 500)		

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
