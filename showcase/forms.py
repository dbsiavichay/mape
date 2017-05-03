# -*- coding: utf-8 -*-
from django import forms

from .models import *

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = '__all__'

	when = forms.DateTimeField(
		input_formats=['%d/%m/%Y %H:%M:%S'], 
		widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M:%S')
	)
