# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from django.contrib.contenttypes.models import ContentType

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import *
from .forms import *

from notifications.models import Notification
from social.models import Profile

class EventListView(ListView):
	model = Event	

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object_list = self.model.objects.filter(
				Q(guest__user=request.user, guest__is_creator=True) | 
				Q(is_public=True)
			)			
			
			events = []

			for event in self.object_list:
				events.append({
					'id': event.id,
					'name': event.name,
					'description': event.description,
					'latitude': event.latitude,
					'longitude': event.longitude
				})

			return JsonResponse(events, safe=False)
		else:
			return super(EventListView, self).get(request, *args, **kwargs)

class EventCreateView(CreateView):
	model = Event
	form_class = EventForm
	success_url = '/map/'

	def get_context_data(self, **kwargs):
		context = super(EventCreateView, self).get_context_data(**kwargs)

		lng = self.request.GET.get('lng') or self.kwargs.get('lng') or None	
		lat = self.request.GET.get('lat') or self.kwargs.get('lat') or None

		localities = Locality.objects.filter(owner=self.request.user)
		reference = Point(float(lng), float(lat))
		close = Locality.objects.filter(point__distance_lte=(reference, D(m=1000)))

		context.update({
			'localities': localities,
			'close':close
		})

		return context

	def form_valid(self, form):
		start = datetime.datetime.combine(
			form.cleaned_data['start_0'],
			form.cleaned_data['start_1']
		)

		self.object = form.save(commit=False)
		self.object.start = start
		self.object.save()

		Guest.objects.create(
			user = self.request.user,
			event = self.object,
			is_creator = True,
			is_organizer = True,
			status = Guest.ATTEND
		)


		self.success_url = '/event/%s/' % (self.object.id)		
		
		return super(EventCreateView, self).form_valid(form)

	def get_form_kwargs(self):	    
		kwargs = super(EventCreateView, self).get_form_kwargs()

		lat = self.request.GET.get('lat') or self.kwargs.get('lat') or None
		lng = self.request.GET.get('lng') or self.kwargs.get('lng') or None		

		initial = {
			'latitude' : lat,
			'longitude': lng			
		}

		kwargs.update({'initial': initial})
		return kwargs

class EventUpdateView(UpdateView):
	model = Event
	form_class = EventForm
	success_url = '/map/'

	def get_context_data(self, **kwargs):
		context = super(EventUpdateView, self).get_context_data(**kwargs)

		lng = self.object.latitude	
		lat = self.object.longitude

		localities = Locality.objects.filter(owner=self.request.user)
		reference = Point(lng, lat)
		close = Locality.objects.filter(point__distance_lte=(reference, D(m=1000)))

		context.update({
			'localities': localities,
			'close':close
		})

		return context

	def form_valid(self, form):
		start = datetime.datetime.combine(
			form.cleaned_data['start_0'],
			form.cleaned_data['start_1']
		)

		self.object = form.save(commit=False)
		self.object.start = start
		self.object.save()

		self.success_url = '/event/%s/' % (self.object.id)		
		
		return redirect(self.success_url)

	def get_form_kwargs(self):
		kwargs = super(EventUpdateView, self).get_form_kwargs()	    
		initial = {
			'start_0': self.object.start.date(),
			'start_1': self.object.start.time()			
		}

		kwargs.update({'initial': initial})
		return kwargs

class EventDetailView(DetailView):
	model = Event

	def get_context_data(self, **kwargs):
		context = super(EventDetailView, self).get_context_data(**kwargs)
		organizers = self.object.guests.filter(guest__user=self.request.user, guest__is_organizer=True)

		context.update({
			'guests': context['event'].guests.filter(guest__status=1),
			'is_organizer': True if len(organizers) > 0 else False
		})

		return context

	def get(self, request, *args, **kwargs):
		#Redirecciona si no es invitado
		self.object = self.get_object()		
		invited = self.object.guests.filter(guest__user=request.user)

		if len(invited) <= 0:
			return redirect('/map/')

		return super(EventDetailView, self).get(request, *args, **kwargs)


class LocalityListView(ListView):
	model = Locality

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			object_list = self.model.objects.filter(Q(owner=request.user) | Q(is_public=True))
			
			localities = []

			for locality in object_list:				
				localities.append({
					'id': locality.id,
					'name': locality.name,
					'description': locality.description,
					'longitude': locality.point.x,
					'latitude': locality.point.y,
				})

			return JsonResponse(localities, safe=False)
		else:
			return super(LocalityListView, self).get(request, *args, **kwargs)

class LocalityCreateView(CreateView):
	model = Locality
	form_class = LocalityForm
	success_url = '/map/'

	def get_context_data(self, **kwargs):
		context = super(LocalityCreateView, self).get_context_data(**kwargs)

		commercial_form = self.get_commercial_form()

		context.update({'commercial_form': commercial_form})

		return context

	def form_valid(self, form):
		commercial_form = self.get_commercial_form()

		print form.cleaned_data.get('is_commercial')

		if form.cleaned_data.get('is_commercial') and commercial_form.is_valid():
			self.object = form.save()
			comm = commercial_form.save(commit=False)
			comm.locality = self.object
			comm.save()
		
		return super(LocalityCreateView, self).form_valid(form)

	def get_commercial_form(self):
		if self.request.method == 'POST':
			commercial_form = CommercialForm(self.request.POST)
		else:
			commercial_form = CommercialForm()

		return commercial_form


	def get_form_kwargs(self):	    
		kwargs = super(LocalityCreateView, self).get_form_kwargs()

		lat = self.request.GET.get('lat') or self.kwargs.get('lat') or None
		lng = self.request.GET.get('lng') or self.kwargs.get('lng') or None		

		initial = {
			'latitude' : lat,
			'longitude': lng			
		}

		kwargs.update({'initial': initial})
		return kwargs

class LocalityDetailView(DetailView):
	model = Locality

	def get_context_data(self, **kwargs):
		context = super(LocalityDetailView, self).get_context_data(**kwargs)
		contenttype = ContentType.objects.get_for_model(Locality)

		try:
			subscriber = Subscriber.objects.get(contenttype=contenttype, user=self.request.user)
		except Subscriber.DoesNotExist:
			subscriber = None

		context.update({
			'contenttype': contenttype,
			'is_subscribed': True if subscriber is not None else False
		})

		return context

###FUNCTION VIEWS###

def add_subscriber(request):
	if request.method == 'POST':
		form = SubscriberForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(form.data.get('next'))
		else:
			print form.errors

def send_invitation(request, event):
	if request.is_ajax() and request.method == 'POST':				
		friends = request.POST.getlist('friends[]')

		for profile_id in friends:

			profile = Profile.objects.get(pk=profile_id)
			Notification.objects.create(
				from_profile = request.user.profile,
				to_profile = profile,				
				type = 3
			)

			Guest.objects.create(
				user=profile.user,
				event_id = event
			)

		return JsonResponse({})
	else:
		pass

