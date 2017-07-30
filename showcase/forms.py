# -*- coding: utf-8 -*-
from django import forms

from django.contrib.gis.geos import Point

from .models import *
from social.models import Subscriber

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ('start','guests')
		widgets = {
			'locality': forms.HiddenInput
		}
	
	start_0 = forms.DateField(
		label = 'Fecha de inicio'
	)

	start_1 = forms.TimeField(
		label = 'Hora de inicio'
	)

	ends_0 = forms.DateField(
		label = 'Fecha de finalización',
		required = False
	)

	ends_1 = forms.TimeField(
		label = 'Hora de finalización',
		required = False
	)	

class LocalityForm(forms.ModelForm):
	class Meta:
		model = Locality
		fields = '__all__'

	is_commercial = forms.BooleanField(
		label='Es localidad comercial',
		required = False
	)

	def save(self, commit=True):
		obj = super(LocalityForm, self).save(commit=False)
		obj.point = Point(obj.longitude, obj.latitude)
		
		if commit:
			obj.save()
		return obj


CommercialForm = forms.modelform_factory(Commercial, fields=('ruc',))

SubscriberForm = forms.modelform_factory(Subscriber, fields='__all__')