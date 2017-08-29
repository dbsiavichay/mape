# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from social.models import *

class ProfilesAdmin(admin.ModelAdmin):
	model = Profile


admin.site.register(Profile, ProfilesAdmin)
# Register your models here.
