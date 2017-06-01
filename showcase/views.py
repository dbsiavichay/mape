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

class EventListView(ListView):
	model = Event	

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			object_list = self.model.objects.filter(Q(published_by=request.user) | Q(is_public=True))
			
			events = []

			for event in object_list:
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

class EventDetailView(DetailView):
	model = Event


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

def add_subscriber(request):
	if request.method == 'POST':
		form = SubscriberForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(form.data.get('next'))
		else:
			print form.errors

