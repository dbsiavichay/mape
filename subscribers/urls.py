# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [    
    url(r'^subscriber/add/$', login_required(SubscriberCreateView.as_view()), name='add_subscriber'),    
    url(r'^subscriber/(?P<pk>\d+)/delete/$', login_required(SubscriberDeleteView.as_view()), name='delete_subscriber'),    
]