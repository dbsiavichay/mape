# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

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
	if width > size:
		percentage = (size / width)
		width = int(width * percentage)
		height = int(height * percentage)
		image = image.resize((width, height), Image.ANTIALIAS)

	image.save(image_field.path)

