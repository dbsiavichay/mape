# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from PIL import Image

class Comment(models.Model):
	content = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='comments/images/',blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	object_id = models.IntegerField()
	contenttype = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
	profile = models.ForeignKey('social.Profile', on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		super(Comment, self).save(*args, **kwargs)

		if self.image:
			process_image(self.image, 1500)


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

