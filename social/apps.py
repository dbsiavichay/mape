# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SocialConfig(AppConfig):
    name = 'social'

    def ready(self):
		import notifications.signals
		import social.signals
    
