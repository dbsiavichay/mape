# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import *
from .forms import *

class EventListView(ListView):
	model = Event	

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			object_list = self.model.objects.filter(published_by=request.user)
			
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
			object_list = self.model.objects.filter(owner=request.user)
			
			localities = []

			for locality in object_list:
				localities.append({
					'id': locality.id,
					'name': locality.name,
					'description': locality.description,
					'latitude': locality.latitude,
					'longitude': locality.longitude
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

