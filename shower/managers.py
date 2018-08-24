from django.db import models
from django.db.models import Q

class ShowerManager(models.Manager):	
	def filter_by_keyword(self, keyword):
		if self.model.__name__ == 'Profile':
			return self.filter(
				Q(user__username__icontains=keyword) | 
				Q(user__first_name__icontains=keyword) | 
				Q(user__last_name__icontains=keyword)
			)
		if self.model.__name__ == 'Locality':
			return self.filter(
				Q(categories__name__icontains=keyword) | 
				Q(name__icontains=keyword) | 
				Q(description__icontains=keyword)
			)

		return self.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
