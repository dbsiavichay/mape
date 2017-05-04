# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
#from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DetailView
#from django.forms import modelform_factory
from .models import *
from .forms import *

class UserCreateView(CreateView):
	model = User
	form_class = UserCreationForm
	success_url = '/login'
	template_name= 'social/signup.html'

	#def form_valid(self, form):	   
	#	self.object = form.save()
	#	auth_login(self.request, self.object)
	#	return redirect(self.get_success_url())
