# -*- coding: utf-8 -*-
from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
	class Meta:
		model = Subscriber
		exclude = ('date','profile')
		widgets = {
			'object_id': forms.HiddenInput,
			'contenttype':forms.HiddenInput,			
		}

	def save(self, profile, commit=True):		
		subscriber = super(SubscriberForm, self).save(commit=False)						
		subscriber.profile = profile
		
		if commit:
			subscriber.save()
			
		return subscriber