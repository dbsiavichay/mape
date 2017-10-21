# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import *

class NotificationListView(ListView):
	model = Notification

	def get_queryset(self):
		queryset = super(NotificationListView, self).get_queryset()
		queryset = queryset.filter(to_profile=self.request.user.profile)		
		qs = queryset.filter(status=Notification.UNREAD)
		qs.update(status=Notification.VIEWED)
		return queryset


####FUNCTION VIEWS#####
def read_notification(request, pk):
	next = request.GET.get('next', None)
	try:
		notification = Notification.objects.get(pk=pk)
	except Notification.DoesNotExist:
		return redirect('notifications')
	notification.status = 2
	notification.save()

	if next is not None:
		return redirect(next)

	return redirect('notifications')


