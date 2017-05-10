from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [                
    url(r'^events/$', login_required(EventListView.as_view()), name='event_list'),
    url(r'^event/add/$', login_required(EventCreateView.as_view()), name='event_create'),
    url(r'^event/(?P<pk>\d+)/$', login_required(EventDetailView.as_view()), name='event_detail'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]