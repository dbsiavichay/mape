# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DetailView, FormView
from .models import *
from .forms import *

class UserCreateView(CreateView):
	model = User
	form_class = UserCreationForm
	success_url = '/'
	template_name= 'social/signup.html'

	#def form_valid(self, form):	   
	#	self.object = form.save()
	#	auth_login(self.request, self.object)
	#	return redirect(self.get_success_url())

class LoginView(FormView):
	template_name= 'social/login.html'
	form_class = AuthenticationForm
	success_url = '/events/'

	def form_valid(self, form):
		auth_login(self.request, form.get_user())
		return super(LoginView, self).form_valid(form)		

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return super(LoginView, self).get(request, *args, **kwargs)
		else:
			return redirect(self.get_success_url())

def logout(request):
	auth_logout(request)
	return redirect('/login/')
