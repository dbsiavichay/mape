from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *



urlpatterns = [	    
    url(r'^notifications/$', login_required(NotificationListView.as_view()), name='notifications'),    
    url(r'^notification/(?P<pk>\d+)/read/$', login_required(read_notification), name='read_notification'),
]
