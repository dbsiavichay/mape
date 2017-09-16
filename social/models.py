# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.contrib.contenttypes.models import ContentType

from notifications.mixins import NotificationMixin

from PIL import Image

class Profile(models.Model):
	charter = models.CharField(max_length=10, blank=True, null=True, verbose_name='cédula')
	birthday = models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')
	cellphone = models.CharField(max_length=32, blank=True, null=True, verbose_name='número de celular')
	avatar = models.ImageField(upload_to='social/avatares/', blank=True, null=True,)	
	is_complete = models.BooleanField(default=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

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

class FriendshipManager(models.Manager):
	def send_request(self, from_profile, to_profile):
		from notifications.models import Notification
		if from_profile == to_profile:
			raise ValidationError("No se puede enviar una solicitud el mismo.")

		friendships = Friendship.objects.filter(
			models.Q(from_profile=from_profile) | models.Q(to_profile=from_profile),
			models.Q(from_profile=to_profile) | models.Q(to_profile=to_profile)
		)

		if len(friendships) > 0:
			return False

		friendship = Friendship.objects.create(
			from_profile = from_profile,
			to_profile = to_profile,
			status = Friendship.FRIENDSHIP_REQUEST
		)

		return friendship

	def accept(self, from_profile, to_profile):
		friendships = Friendship.objects.filter(from_profile=from_profile, to_profile=to_profile)
		if len(friendships) != 1:
			raise ValidationError('Error de integridad')

		friendship = friendships[0]

		friendship.status = Friendship.FRIENDSHIP_FRIEND
		friendship.save()
		return True

	def reject(self, from_profile, to_profile):
		friendships = Friendship.objects.filter(
			from_profile=from_profile, to_profile=to_profile, status=Friendship.FRIENDSHIP_REQUEST
		)
		if len(friendships) != 1:
			raise ValidationError('Error de integridad')

		friendships.delete()
		return True

	def delete_friend(self, profile1, profile2):
		friendships = Friendship.objects.filter(
			models.Q(from_profile=profile1) | models.Q(to_profile=profile1),
			models.Q(from_profile=profile2) | models.Q(to_profile=profile2)
		).filter(status=Friendship.FRIENDSHIP_FRIEND)

		friendships.delete()
		return True

	
	def check_status(self, profile1, profile2, check=True):
		friendships = Friendship.objects.filter(
			from_profile=profile1, to_profile=profile2			
		)

		if len(friendships) == 0:
			return self.check_status(profile2, profile1, check=False) if check else 'Envia una solicitud'
		
		friendship = friendships[0]

		if friendship.status == Friendship.FRIENDSHIP_REQUEST:
			return 'Solicitud enviada.' if check else 'Solicitud recibida.'
		elif friendship.status == Friendship.FRIENDSHIP_FRIEND:
			return 'Amigos'
		else:
			return 'Bloqueado'

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

class Subscriber(models.Model):
	object_id = models.IntegerField()
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)		

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
