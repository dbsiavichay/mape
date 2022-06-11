# -*- coding: utf-8 -*-
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [    
    path(r'^subscriber/add/$', login_required(SubscriberCreateView.as_view()), name='add_subscriber'),    
    path(r'^subscriber/(?P<pk>\d+)/delete/$', login_required(SubscriberDeleteView.as_view()), name='delete_subscriber'),    
]