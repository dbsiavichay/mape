# -*- coding: utf-8 -*-
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('date','profile')
		widgets = {
			'object_id': forms.HiddenInput,
			'contenttype':forms.HiddenInput,			
		}

	def save(self, profile, commit=True):		
		comment = super(CommentForm, self).save(commit=False)						
		comment.profile = profile
		
		if commit:
			comment.save()
			
		return comment