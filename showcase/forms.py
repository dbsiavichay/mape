# -*- coding: utf-8 -*-
from django import forms

from .models import *

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ('start',)
	
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


CommercialForm = forms.modelform_factory(Commercial, fields=('ruc',))