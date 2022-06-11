# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from social.models import Profile

class Notification(models.Model):	
	UNREAD = 1
	VIEWED = 2
	READ = 3
		
	TYPE_CHOICES = (
		(1, 'Like'),
		(2, 'Amistad'),
		(3, 'Invitacion'),		
	)

	STATUS_CHOICES = (
		(UNREAD, 'Sin leer'),
		(VIEWED, 'Visto'),
		(READ, 'Leida'),
	)

	from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
	message = models.TextField(blank=True, null=True)
	#type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)	
	url = models.CharField(max_length=256, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
	object_id = models.PositiveSmallIntegerField()
	contenttype = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
