# -*- coding: utf-8 -*-
from django.db import models

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
