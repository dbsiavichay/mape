from django.test import TestCase

import datetime
from django.utils import timezone
from social.models import * 

class UserMagagementTests(TestCase):
	def test_birthday_with_future_date(self) 
	time = timezone.now() + datetime.timedelta(years=13)
	future_date = Profile(birthday=time)

	self.assertIs(future_date.test_birthday_with_future_date(), False)
	