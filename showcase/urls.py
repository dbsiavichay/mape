from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
	url(r'^$', MapView.as_view(), name='map'),
    url(r'^events/$', EventListView.as_view(), name='event_list'),
    url(r'^event/add/$', login_required(EventCreateView.as_view()), name='event_create'),
    url(r'^event/(?P<pk>\d+)/update/$', login_required(EventUpdateView.as_view()), name='event_update'),
    url(r'^event/(?P<pk>\d+)/$', login_required(EventDetailView.as_view()), name='event_detail'),
    url(r'^event/(?P<pk>\d+)/cancel/$', login_required(cancel_event), name='event_cancel'),

    
    url(r'^event/(?P<pk>\d+)/attend/$', login_required(event_attend), name='event_attend'),
    url(r'^event/(?P<pk>\d+)/like/$', login_required(event_like), name='event_like'),
    url(r'^event/(?P<pk>\d+)/maybe_attend/$', login_required(event_maybe_attend), name='event_maybe_attend'),
    url(r'^event/(?P<pk>\d+)/not_attend/$', login_required(event_not_attend), name='event_not_attend'),

    url(r'^localities/$', LocalityListView.as_view(), name='locality_list'),
    url(r'^locality/add/$', login_required(LocalityCreateView.as_view()), name='locality_create'),
    url(r'^locality/(?P<pk>\d+)/update/$', login_required(LocalityUpdateView.as_view()), name='locality_update'),
    url(r'^locality/(?P<pk>\d+)/$', LocalityDetailView.as_view(), name='locality_detail'),    
    url(r'^locality/(?P<pk>\d+)/map/$', LocalityMapView.as_view(), name='locality_map'),    
    

    url(r'^commercial/$', login_required(CommercialUpdateView.as_view()), name='commercial_update'),    
    url(r'^commercial/offers/$', login_required(OfferCreateView.as_view()), name='offer_create'),    
    url(r'^commercial/offers/(?P<pk>\d+)/update/$', login_required(OfferUpdateView.as_view()), name='offer_update'),    

    url(r'^event/(?P<event>\d+)/invitation/$', login_required(event_invitation), name='event_invitation'),
    url(r'^event/(?P<event>\d+)/sponsor-request/$', login_required(event_sponsor), name='sponsor_invitation'),
    url(r'^event/(?P<event>\d+)/sponsor-request/accept/$', login_required(event_sponsor_accept), name='sponsor_accept'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]