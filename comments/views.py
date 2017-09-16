# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView
from .models import Comment
from .forms import CommentForm

class CommentCreateView(CreateView):
	#http_method_names = [u'get', u'post', u'put', u'delete', u'head', u'options', u'trace']
	http_method_names = [u'post', u'put', ]
	model = Comment
	form_class = CommentForm

	def form_valid(self, form):
		self.object = form.save(self.request.user.profile)		
		next = self.object.contenttype.get_object_for_this_type(pk=self.object.object_id)

		return redirect(next.get_absolute_url())

class CommentDeleteView(DeleteView):
	http_method_names = [u'post', u'put', ]
	model = Comment	

	def delete(self, request, *args, **kwargs):	    
	    self.object = self.get_object()
	    self.object.delete()
	    next = self.object.contenttype.get_object_for_this_type(pk=self.object.object_id)

	    return redirect(next.get_absolute_url())
