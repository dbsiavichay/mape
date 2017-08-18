from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

from django.views.generic import TemplateView

urlpatterns = [
	#url(r'^$', TemplateView.as_view(template_name='social/home.html'), name='home'),
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    url(r'^logout/$', login_required(logout), name='logout'),
    url(r'^profiles/(?P<username>[\w.@+-]+)/$', login_required(ProfileUpdateView.as_view()), name='profile_update'),
    url(r'^profiles/(?P<username>[\w.@+-]+)/friends/$', login_required(RelationshipListView.as_view()), name='relationship'),
    url(r'^profiles/send-request/(?P<target>\d+)/$', login_required(send_request), name='profile_send_request'),
    url(r'^profiles/request/accept/(?P<target>\d+)/$', login_required(accept_request), name='profile_accept_request'),
    url(r'^profiles/request/reject/(?P<target>\d+)/$', login_required(reject_request), name='profile_reject_request'),
    
    url(r'^profiles/set/commercial-account/$', login_required(CommercialAccountView.as_view()), name='commercial_account'),    
    #url(r'^user/profile/$', login_required(UserProfileView.as_view()), name='user_profile'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]
