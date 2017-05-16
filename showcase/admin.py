# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    model = Category

admin.site.register(Category, CategoryAdmin)