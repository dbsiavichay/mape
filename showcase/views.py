# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.shortcuts import render
from django.views.generic import ListView, CreateView
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
	fields = '__all__'
	success_url = '/events/'

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

