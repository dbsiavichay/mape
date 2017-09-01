# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import *

class NotificationListView(ListView):
	model = Notification


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


