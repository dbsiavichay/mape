# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView
from django.shortcuts import render, redirect

from django.contrib.contenttypes.models import ContentType
from showcase.models import *

class ShowerListView(ListView):
	model = Event
	template_name = 'shower/shower_list.html'

	def get_context_data(self, **kwargs):
		list_of_models = ['event', 'locality', 'profile', 'offer']

		context = super(ShowerListView, self).get_context_data(**kwargs)
		keyword = self.request.GET.get('keyword') or kwargs.get('keyword') or None				
		model = self.request.GET.get('model') or self.kwargs.get('model') or None


		context.update({
			'keyword':keyword,
			'model':model if model in list_of_models else 'all',			
		})

		return context