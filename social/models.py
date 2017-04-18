# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    birthday = models.DateField(null=True, blank=True)        
    cellphone = models.CharField(blank=True, null=True)
    avatar = models.ImageField(upload_to='social/avatares/', null=True, blank=True)    
    user = models.OneToOneField(User)    

    def __unicode__(self):
    	return unicode(self.user.username)
