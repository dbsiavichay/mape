# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from datetime import timedelta, date
import locale

from django.http import JsonResponse

from django.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D


from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from .models import *
from .forms import *

from social.models import Profile

class MapView(TemplateView):
	template_name='showcase/map.html'	

class EventListView(ListView):
	model = Event	

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			profile = request.user.profile if not request.user.is_anonymous() else None
			today_number = datetime.datetime.weekday(datetime.datetime.now()) 
			monday_date = datetime.datetime.today() - timedelta(days=today_number) 
			tuesday = monday_date + timedelta(days=1)
			wednesday = monday_date + timedelta(days=2)
			thursday = monday_date + timedelta(days=3)
			friday = monday_date + timedelta(days=4)
			saturday = monday_date + timedelta(days=5)
			sunday = monday_date + timedelta(days=6)

			self.object_list = self.model.objects.filter(
				Q(start__day=monday_date.day) |
				Q(start__day=tuesday.day) |
				Q(start__day=wednesday.day) |
				Q(start__day=thursday.day) |
				Q(start__day=friday.day) |
				Q(start__day=saturday.day) |
				Q(start__day=sunday.day),
				Q(guest__profile=profile) | 
				Q(is_public=True)
			).exclude(status=2).exclude(status=3)			
			
			events = []

			for event in self.object_list:
				dic_days = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miércoles','THURSDAY':'Jueves', \
				'FRIDAY':'Viernes','SATURDAY':'Sábado','SUNDAY':'Domingo'}
				
				day = dic_days[event.start.strftime('%A').upper()]

				events.append({
					'event_id': event.id,
					'owner_id': event.owner().id if not event.is_public else event.owner().commercial().locality.id,
					'name': event.name,
					'description': event.description,
					'latitude': event.latitude,
					'longitude': event.longitude,
					'event_image_url': event.front_image.url if event.front_image else '#',
					'event_owner': event.owner().user.username if not event.is_public else event.owner().commercial().locality.name,
					'day': day,
					'status': event.status,
					'is_public': event.is_public,
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
		lat = lat.replace(",", ".")
		lng = lng.replace(",", ".")
		localities = Locality.objects.filter(owner=self.request.user.profile)
		reference = Point(float(lng), float(lat))
		close = Locality.objects.filter(point__distance_lte=(reference, D(m=150)))

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
			is_owner = True,			
			status = Guest.ATTEND
		)


		self.success_url = '/event/%s/' % (self.object.id)				
		return redirect(self.success_url)

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
		owners = self.object.guests.filter(guest__profile=self.request.user.profile, guest__is_owner=True)
		sponsors = self.object.guests.filter(guest__is_sponsor=True)
		sponsors_request = self.object.guests.filter(guest__profile=self.request.user.profile, guest__status=Guest.SPONSOR_REQUEST)
		commercials = Commercial.objects.exclude(locality__owner=self.request.user.profile)		

		context.update({
			'guests': context['event'].guests.filter(guest__is_owner=False),
			'is_owner': True if len(owners) > 0 else False,
			'sponsors': sponsors,
			'is_sponsor_request': True if len(sponsors_request) > 0 else False,
			'commercials':commercials
		})

		return context

	def get(self, request, *args, **kwargs):
		#Redirecciona si no es invitado
		self.object = self.get_object()
		if self.object.is_public:
			return super(EventDetailView, self).get(request, *args, **kwargs)

		invited = self.object.guests.filter(guest__profile=request.user.profile)

		if len(invited) > 0:
			return super(EventDetailView, self).get(request, *args, **kwargs)
		
		return redirect('/map/')

def cancel_event(request, pk):
	try:
		event = Event.objects.get(pk=pk)
	except Event.DoesNotExist:
		return redirect('map')
	event.status = 3
	event.save()
	return redirect(event.get_absolute_url())

class EventMapView(DetailView):
	model = Event
	template_name = 'showcase/map.html'	

	def get_context_data(self, **kwargs):
	    context = super(EventMapView, self).get_context_data(**kwargs)	    

	    context.update({
	    	'lat': self.object.latitude,
	    	'lng': self.object.longitude
	    })

	    return context

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
					'locality_image_url': locality.profile_image.url if locality.profile_image else '#',
					'owner_name': locality.owner.user.username,
					'owner_image_url': locality.owner.avatar.url if locality.owner.avatar else '#', 
					'verified': locality.verified,
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
	slug_field = 'id'
	slug_url_kwarg = 'id'

	def get_context_data(self, **kwargs):
	    context = super(LocalityDetailView, self).get_context_data(**kwargs)	    

	    context.update({
	    	'lat': self.object.latitude,
	    	'lng': self.object.longitude
	    })

	    return context

class LocalityMapView(DetailView):
	model = Locality
	template_name = 'showcase/map.html'	

	def get_context_data(self, **kwargs):
	    context = super(LocalityMapView, self).get_context_data(**kwargs)	    

	    context.update({
	    	'lat': self.object.latitude,
	    	'lng': self.object.longitude
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
			'services': services,
			'locality': self.object.locality
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
		kind = 	self.request.GET.get('kind') or self.kwargs.get('kind') or None
		kwargs = super(OfferCreateView, self).get_form_kwargs()	
		initial = {
			'kind':kind,
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
	event = Event.objects.get(pk=pk)
	try:
		invitation = Guest.objects.get(profile=request.user.profile, event=event)
		invitation.status = Guest.ATTEND
		invitation.save()
	except Guest.DoesNotExist:
		Guest.objects.create(
			profile=request.user.profile,
			event=event,
			status=Guest.ATTEND
		)	

	return redirect('/event/%s/' % pk)

def event_maybe_attend(request, pk):
	event = Event.objects.get(pk=pk)
	try:
		invitation = Guest.objects.get(profile=request.user.profile, event=event)
		invitation.status = Guest.MAYBE_ATTEND
		invitation.save()
	except Guest.DoesNotExist:
		Guest.objects.create(
			profile=request.user.profile,
			event=event,
			status=Guest.MAYBE_ATTEND
		)	

	return redirect('/event/%s/' % pk)

def event_not_attend(request, pk):
	event = Event.objects.get(pk=pk)
	try:
		invitation = Guest.objects.get(profile=request.user.profile, event=event)
		invitation.status = Guest.NOT_ATTEND
		invitation.save()
	except Guest.DoesNotExist:
		Guest.objects.create(
			profile=request.user.profile,
			event=event,
			status=Guest.NOT_ATTEND
		)

	return redirect('/event/%s/' % pk)

def event_invitation(request, event):
	if request.is_ajax() and request.method == 'POST':				
		friends = request.POST.getlist('friends[]')

		for profile_id in friends:

			profile = Profile.objects.get(pk=profile_id)
			
			Guest.objects.create(
				profile=profile,
				event_id = event
			)

		return JsonResponse({})
	else:
		pass

def event_sponsor(request, event):
	if request.is_ajax() and request.method == 'POST':				
		commercials = request.POST.getlist('commercials[]')
		
		for id in commercials:
			commercial = Commercial.objects.get(pk=id)

			Guest.objects.create(
				profile=commercial.locality.owner,
				event_id = event,
				status = Guest.SPONSOR_REQUEST
			)

		return JsonResponse({})
	else:
		pass

def event_sponsor_accept(request, event):
	event = Event.objects.get(pk=event)
	profile = request.user.profile

	invitation = Guest.objects.get(profile = profile, status = Guest.SPONSOR_REQUEST)
	invitation.status = Guest.ATTEND
	invitation.is_sponsor = True
	invitation.save()

	subscribers = profile.commercial().locality.subscribers()

	for subscriber in subscribers:
		Guest.objects.create(
			profile=subscriber.profile,
			event = event
		)

	return redirect('event_detail', pk=event.id)

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