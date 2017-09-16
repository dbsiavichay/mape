# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView
from .models import Subscriber
from .forms import SubscriberForm

class SubscriberCreateView(CreateView):	
	http_method_names = [u'post', u'put', ]
	model = Subscriber
	form_class = SubscriberForm

	def form_valid(self, form):
		self.object = form.save(self.request.user.profile)		
		next = self.object.contenttype.get_object_for_this_type(pk=self.object.object_id)

		return redirect(next.get_absolute_url())

class SubscriberDeleteView(DeleteView):
	http_method_names = [u'post', u'put', ]
	model = Subscriber	

	def delete(self, request, *args, **kwargs):	    
	    self.object = self.get_object()
	    self.object.delete()
	    next = self.object.contenttype.get_object_for_this_type(pk=self.object.object_id)

	    return redirect(next.get_absolute_url())

