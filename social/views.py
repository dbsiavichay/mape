# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
#------------------------------------------------------------------------
from django.http import JsonResponse
#------------------------------------------------------------------------
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from .models import *
from .forms import *

from showcase.forms import CommercialAccountForm
from showcase.models import Locality



class UserCreateView(CreateView):
	model = User
	form_class = UserCreationForm
	success_url = '/'
	template_name= 'social/signup.html'

	def form_valid(self, form):
		from .mails import send_activate_account
		self.object = form.save()
		user = authenticate(
			username=form.cleaned_data['username'], 
			password=form.cleaned_data['password1']
		)
		auth_login(self.request, user)
		#send_activate_account(self.object)
		return redirect(self.success_url+'?action=emailsend')

#------------------------------------------------------------------------
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def FConnectionView(request):
	profile = None
	if request.is_ajax() and request.method == 'POST' and not request.user.is_authenticated():
		profile = request.POST.get('profile')
		duplicate = User.objects.filter(username__iexact=profile).exists()
		print duplicate
	if profile and duplicate:
		instance = User.objects.get(username__iexact=profile)
		#instance = User.objects.get(email__iexact=profile)
		if instance:
			user = authenticate( 
			username='pepe', 
			password='pepepass')
			auth_login(request, user)
			return JsonResponse({'url': '/'}) 
	elif profile: 
		instance = User.objects.create_user('pruebadef', 'correo@gmail.com', 'userpass')
		instance.save() 
		user = authenticate( 
		username='pruebadef', 
		password='userpass')
		auth_login(request, user)
		return JsonResponse({'url': '/'})

#------------------------------------------------------------------------
class ActivateAccountView(DetailView):
	model = Profile
	slug_field = 'user__username'
	slug_url_kwarg = 'username'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.active_by_email = True
		self.object.save()

		return redirect('/'+'?action=activationsuccess')

class LoginView(FormView):
	template_name= 'social/login.html'
	form_class = AuthenticationForm
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)

		action = self.request.GET.get('action') or self.kwargs.get('action') or None

		context.update({
			'action': action
		})

		return context

	def form_valid(self, form):
		user = form.get_user()		
		#if not user.profile.active_by_email:
		#	return redirect('/' + '?emailsend=true')

		auth_login(self.request, user)
		next_param = self.request.GET.get('next') or self.kwargs.get('next') or None		
		if next_param is not None:
			self.success_url = next_param
		return redirect(self.success_url)

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
	fields = ('username', 'email')	
	template_name = 'social/profile_form.html'	

	def get_context_data(self, **kwargs):
		context = super(ProfileUpdateView, self).get_context_data(**kwargs)		
		context['profile_form'] = self.get_profile_form()
		success = self.request.GET.get('success') or kwargs.get('success') or None
		commercial = self.request.GET.get('commercial') or kwargs.get('commercial') or None
		if success is not None: context['success'] = success
		if commercial is not None: context['commercial'] = commercial
		return context

	def form_valid(self, form):
		profile_form = self.get_profile_form()
		if profile_form.is_valid():						
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			profile_form.save(username, email)
			
			self.success_url = '/profiles/%s/?success=true' % username
			return redirect(self.success_url)
			
		return self.form_invalid(form)

	def get_profile_form(self):
		profile = self.request.user.profile
		form = ProfileForm(instance=profile)

		if self.request.method == 'POST':
			form = ProfileForm(self.request.POST, self.request.FILES, instance=profile)

		return form
		
	def get_object(self, queryset=None):		
		return self.request.user


class ProfileDetailView(DetailView):
	model = Profile
	slug_field = 'user__username'
	slug_url_kwarg = 'username'

	def get_context_data(self, **kwargs):
		context = super(ProfileDetailView, self).get_context_data(**kwargs)
		profile = self.request.user.profile

		relationship = profile.get_status_with_profile(self.object)

		if relationship is None: return context

		if relationship.status == 1:
			context.update({
				'status': 'send' if relationship.from_profile == profile else 'received'
			})	
		else:
			context.update({
				'status': 'friend'
			})

		return context

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
			).exclude(user=self.request.user)

			for profile in objects:
				text = Friendship.objects.check_status(self.request.user.profile, profile)
				profiles.append((text, profile))			

			context.update({
				'profiles': profiles,				
			})

		return context	


def send_request(request, target):
	target = Profile.objects.get(pk=target)
	Friendship.objects.send_request(request.user.profile, target)

	keyword = request.GET.get('keyword', '')
	return redirect('/profiles/%s/friends/?keyword=%s' % (request.user.username, keyword))

def accept_request(request, target):
	target = Profile.objects.get(pk=target)	
	Friendship.objects.accept(target, request.user.profile)

	keyword = request.GET.get('keyword', '')
	return redirect('/profiles/%s/friends/?keyword=%s' % (request.user.username, keyword))

def reject_request(request, target):
	target = Profile.objects.get(pk=target)
	Friendship.objects.reject(target, request.user.profile)
	keyword = request.GET.get('keyword', '')

	return redirect('/profiles/%s/friends/?keyword=%s' % (request.user.username, keyword))

def delete_request(request, target):
	target = Profile.objects.get(pk=target)
	Friendship.objects.reject(request.user.profile, target)
	keyword = request.GET.get('keyword', '')

	return redirect('/profiles/%s/friends/?keyword=%s' % (request.user.username, keyword))

def delete_friend(request, target):
	target = Profile.objects.get(pk=target)
	profile = request.user.profile

	Friendship.objects.delete_friend(profile, target)
	return redirect('relationship', username=request.user.username)
	
class CommercialAccountView(UpdateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'social/commercial_account.html'
	success_url = '/commercial/'

	def form_valid(self, form):
		commercial_form = self.get_commercial_form()

		if commercial_form.is_valid():			
			self.object = form.save()
			commercial = commercial_form.save()
			commercial.locality.owner = self.request.user.profile
			commercial.locality.save()
			
			return redirect('commercial_update')			
			
		return self.form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super(CommercialAccountView, self).get_context_data(**kwargs)

		#success = self.request.GET.get('success') or self.kwargs.get('success') or None
		commercial_form = self.get_commercial_form()
		context.update({			
			'commercial_form':commercial_form,
		#	'success': success
		})

		return context

	def get_commercial_form(self):
		current_profile = self.request.user.profile	
		instance = current_profile.commercial()
		form = CommercialAccountForm(instance=instance, profile=current_profile)
		if self.request.method == 'POST':
			form = CommercialAccountForm(self.request.POST, self.request.FILES, instance=instance, profile=current_profile)

		return form

	def get(self, request, *args, **kwargs):
		print request.user.profile.commercial()
		if request.user.profile.commercial() is not None:
			return redirect('map')

		return super(CommercialAccountView, self).get(request, *args, **kwargs)

	def get_object(self, queryset=None):
		return self.request.user.profile

def ConditionsView(request):
	return render(request, 'showcase/components/conditions.html')

def PrinciplesView(request):
	return render(request, 'showcase/components/principles.html')
	
def PoliticsView(request):
	return render(request, 'showcase/components/politics.html')