# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
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
	success_url = '/map/'

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
	return redirect('/')

class ProfileUpdateView(UpdateView):
	model = User
	fields = ('username', 'first_name', 'last_name', 'email')	
	template_name = 'social/profile_form.html'	

	def get_context_data(self, **kwargs):
		context = super(ProfileUpdateView, self).get_context_data(**kwargs)		
		context['profile_form'] = self.get_profile_form()
		success = self.request.GET.get('success') or kwargs.get('success') or None
		if success is not None: context['success'] = success
		return context

	def form_valid(self, form):
		profile_form = self.get_profile_form()
		if profile_form.is_valid():
			self.object = form.save()
			profile_form.save()
			self.success_url = '/profiles/%s/?success=true' % (self.request.user.username)
			return super(ProfileUpdateView, self).form_valid(form)			
			
		return self.form_invalid(form)

	def get_profile_form(self):
		profile = self.request.user.profile
		form = ProfileForm(instance=profile)

		if self.request.method == 'POST':
			form = ProfileForm(self.request.POST, self.request.FILES, instance=profile)

		return form
		
	def get_object(self, queryset=None):
		return self.request.user

class RelationshipListView(ListView):
	model = Profile
	template_name = 'social/relationship.html'

	def get_context_data(self, **kwargs):
		context = super(RelationshipListView, self).get_context_data(**kwargs)

		keyword = self.request.GET.get('keyword') or self.kwargs.get('keyword') or None

		if keyword is not None:
			profiles = []
			objects = Profile.objects.filter(
				Q(user__first_name__icontains=keyword) |
				Q(user__last_name__icontains=keyword) |
				Q(user__username__icontains=keyword)
			)

			for profile in objects:
				is_friend = profile.get_relationship(self.request.user.profile, 2)
				have_request = profile.get_relationship(self.request.user.profile, 1)

				if is_friend:
					text = 'Son amigos'
				elif have_request:
					text = 'Solicitud enviada'
				else:
					text = 'Enviale una solicitud'
				 
				can_do_request = not is_friend and not have_request

				profiles.append((text, can_do_request,profile))

			context.update({
				'profiles': profiles
			})

		return context		
