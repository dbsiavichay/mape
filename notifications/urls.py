from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *



urlpatterns = [	    
    path(r'^notifications/$', login_required(NotificationListView.as_view()), name='notifications'),    
    path(r'^notification/(?P<pk>\d+)/read/$', login_required(read_notification), name='read_notification'),
]
