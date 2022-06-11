from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
	path('', MapView.as_view(), name='map'),
    path(r'^events/$', EventListView.as_view(), name='event_list'),
    path(r'^event/add/$', login_required(EventCreateView.as_view()), name='event_create'),
    path(r'^event/(?P<pk>\d+)/update/$', login_required(EventUpdateView.as_view()), name='event_update'),
    path(r'^event/(?P<pk>\d+)/$', login_required(EventDetailView.as_view()), name='event_detail'),
    path(r'^event/(?P<pk>\d+)/cancel/$', login_required(cancel_event), name='event_cancel'),

    
    path(r'^event/(?P<pk>\d+)/attend/$', login_required(event_attend), name='event_attend'),
    path(r'^event/(?P<pk>\d+)/like/$', login_required(event_like), name='event_like'),
    path(r'^event/(?P<pk>\d+)/maybe_attend/$', login_required(event_maybe_attend), name='event_maybe_attend'),
    path(r'^event/(?P<pk>\d+)/not_attend/$', login_required(event_not_attend), name='event_not_attend'),
    path(r'^event/(?P<pk>\d+)/map/$', login_required(EventMapView.as_view()), name='event_map'),

    path(r'^localities/$', LocalityListView.as_view(), name='locality_list'),
    path(r'^locality/add/$', login_required(LocalityCreateView.as_view()), name='locality_create'),
    path(r'^locality/(?P<pk>\d+)/update/$', login_required(LocalityUpdateView.as_view()), name='locality_update'),
    
    #path(r'^locality/(?P<pk>\d+)/$', LocalityDetailView.as_view(), name='locality_detail'),
    path(r'^locality/(?P<name>[\w.@+-]+)/$', LocalityDetailView.as_view(), name='locality_detail'),

    path(r'^locality/(?P<pk>\d+)/map/$', LocalityMapView.as_view(), name='locality_map'),    
    

    path(r'^commercial/$', login_required(CommercialUpdateView.as_view()), name='commercial_update'),    
    path(r'^commercial/offers/$', login_required(OfferCreateView.as_view()), name='offer_create'),    
    path(r'^commercial/offers/(?P<pk>\d+)/update/$', login_required(OfferUpdateView.as_view()), name='offer_update'),    

    path(r'^event/(?P<event>\d+)/invitation/$', login_required(event_invitation), name='event_invitation'),
    path(r'^event/(?P<event>\d+)/sponsor-request/$', login_required(event_sponsor), name='sponsor_invitation'),
    path(r'^event/(?P<event>\d+)/sponsor-request/accept/$', login_required(event_sponsor_accept), name='sponsor_accept'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]