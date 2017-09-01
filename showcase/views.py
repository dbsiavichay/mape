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
			profile = request.user.profile if not request.user.is_anonymous() else None

			self.object_list = self.model.objects.filter(
				Q(guest__profile=profile) | 
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

		localities = Locality.objects.filter(owner=self.request.user.profile)
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
			profile = self.request.user.profile,
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

		localities = Locality.objects.filter(owner=self.request.user.profile)
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
		organizers = self.object.guests.filter(guest__profile=self.request.user.profile, guest__is_organizer=True)

		context.update({
			'guests': context['event'].guests.filter(guest__is_creator=False),
			'is_organizer': True if len(organizers) > 0 else False
		})

		return context

	def get(self, request, *args, **kwargs):
		#Redirecciona si no es invitado
		self.object = self.get_object()		
		invited = self.object.guests.filter(guest__profile=request.user.profile)

		if len(invited) <= 0:
			return redirect('/map/')

		return super(EventDetailView, self).get(request, *args, **kwargs)


class LocalityListView(ListView):
	model = Locality

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			profile = request.user.profile if not request.user.is_anonymous() else None
			
			object_list = self.model.objects.filter(Q(owner=profile) | Q(is_public=True))
						
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

	def form_valid(self, form):			
		self.object = form.save()		
		return redirect('locality_detail', pk=self.object.id)

	def post(self, request, *args, **kwargs):
		request.POST = create_categories(request.POST.getlist('categories'), request.POST.copy())
		return super(LocalityCreateView, self).post(request, *args, **kwargs)

	def get_form_kwargs(self):	    
	## Recogemos las palabras clave recurrentemente en lat y lng
		kwargs = super(LocalityCreateView, self).get_form_kwargs()

		lat = self.request.GET.get('lat') or self.kwargs.get('lat') or None
		lng = self.request.GET.get('lng') or self.kwargs.get('lng') or None		

		initial = {
			'latitude' : lat,
			'longitude': lng,
			'owner': self.request.user.profile,			
		}

		kwargs.update({'initial': initial})
		return kwargs

class LocalityUpdateView(UpdateView):
	model = Locality
	#fields = '__all__'
	form_class = LocalityForm
	success_url = '/map/'

	def form_valid(self, form):		
		self.object = form.save()
		return redirect('locality_detail', pk=self.object.id)

	def post(self, request, *args, **kwargs):
		request.POST = create_categories(request.POST.getlist('categories'), request.POST.copy())
		return super(LocalityUpdateView, self).post(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		if self.object.is_commercial:
			return redirect('commercial_update')

		return super(LocalityUpdateView, self).get(request, *args, **kwargs)
	

class LocalityDetailView(DetailView):
	model = Locality

	def get_context_data(self, **kwargs):
		context = super(LocalityDetailView, self).get_context_data(**kwargs)
		contenttype = ContentType.objects.get_for_model(Locality)

		subscriber = None
		if not self.request.user.is_anonymous():
			try:
				subscriber = Subscriber.objects.get(
					contenttype=contenttype, profile=self.request.user.profile, object_id=self.object.id
				)
			except Subscriber.DoesNotExist:
				subscriber = None		

		context.update({
			'contenttype': contenttype,
			'is_subscribed': True if subscriber is not None else False
		})

		return context

class CommercialUpdateView(UpdateView):
	model = Commercial
	form_class = CommercialForm
	template_name = 'showcase/commercial.html'

	def form_valid(self, form):
		locality_form = self.get_locality_form()
		if locality_form.is_valid():
			locality_form.save()
			self.object = form.save()
			return redirect('commercial_update')

		return self.form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super(CommercialUpdateView, self).get_context_data(**kwargs)

		locality_form = self.get_locality_form()
		products = Offer.objects.filter(kind=Offer.PRODUCT, commercial=self.object)
		services = Offer.objects.filter(kind=Offer.SERVICE, commercial=self.object)
		context.update({
			'locality_form': locality_form,
			'products': products,
			'services': services
		})

		return context

	def get_locality_form(self):
		instance = self.object.locality
		form = LocalityForm(instance=instance)

		if self.request.method == 'POST':
			form = LocalityForm(self.request.POST, self.request.FILES, instance=instance)

		return form

	def get(self, request, *args, **kwargs):
		if request.user.profile.commercial() is None:
			return redirect('map')

		return super(CommercialUpdateView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		request.POST = create_categories(request.POST.getlist('categories'), request.POST.copy())
		return super(CommercialUpdateView, self).post(request, *args, **kwargs)

	def get_object(self, queryset=None):
		return self.request.user.profile.commercial()

class OfferCreateView(CreateView):
	model = Offer
	form_class = OfferForm
	success_url = '/commercial/'

	def get_form_kwargs(self):	    		
		kwargs = super(OfferCreateView, self).get_form_kwargs()	
		initial = {			
			'commercial': self.request.user.profile.commercial(),			
		}

		kwargs.update({'initial': initial})
		return kwargs

class OfferUpdateView(UpdateView):
	model = Offer
	form_class = OfferForm
	success_url = '/commercial/'
	
###FUNCTION VIEWS###

def event_like(request, pk):
	invitation = Guest.objects.get(profile=request.user.profile, event=pk)
	invitation.status = Guest.LIKE
	invitation.save()

	return redirect('/event/%s/' % pk)

def event_attend(request, pk):
	invitation = Guest.objects.get(profile=request.profile, event=pk)
	invitation.status = Guest.ATTEND
	invitation.save()

	return redirect('/event/%s/' % pk)

def event_maybe_attend(request, pk):
	invitation = Guest.objects.get(profile=request.profile, event=pk)
	invitation.status = Guest.MAYBE_ATTEND
	invitation.save()

	return redirect('/event/%s/' % pk)

def event_not_attend(request, pk):
	invitation = Guest.objects.get(profile=request.profile, event=pk)
	invitation.status = Guest.NOT_ATTEND
	invitation.save()

	return redirect('/event/%s/' % pk)

def add_event_comment(request):
	if request.method != 'POST':
		return redirect('/map/')

	contenttype = ContentType.objects.get_for_model(Event)
	object_id = request.POST.get('event')
	text = request.POST.get('text', '') 
	image = request.FILES.get('image', None)
	profile = request.user.profile

	Comment.objects.create(text = text, image=image,profile = profile, object_id = object_id, contenttype = contenttype)

	return redirect('/event/%s/' % object_id)

def add_locality_comment(request):
	if request.method != 'POST':
		return redirect('/map/')

	contenttype = ContentType.objects.get_for_model(Locality)
	object_id = request.POST.get('locality')
	text = request.POST.get('text', '') 
	image = request.FILES.get('image', None)
	profile = request.user.profile

	Comment.objects.create(text = text, image=image,profile = profile, object_id = object_id, contenttype = contenttype)

	return redirect('/locality/%s/' % object_id)

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
				profile=profile,
				event_id = event
			)

		return JsonResponse({})
	else:
		pass

###Utilities

def create_categories(category_list, post=None):	
	categories = [cat for cat in category_list if cat.isdigit()]
	
	for cat in category_list:
		if not cat.isdigit():
			category, created = Category.objects.get_or_create(name=cat.encode('utf-8'))
			categories.append(str(category.id))

	#Si hay post se devuelve el post con unicode utf-8 y seteada las categorias
	#De no ser asi solo se devuelve el listado de categorias
	if post is not None:
		##Encode utf-8
		for key in post.keys():
			post[key] = unicode(post[key]).encode('utf-8')

		post.setlist('categories', categories)
		return post

	return categories