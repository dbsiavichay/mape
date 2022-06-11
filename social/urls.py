from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

from django.views.generic import TemplateView

urlpatterns = [	
    path(r'^login/$', LoginView.as_view(), name='login'),
   
    path(r'^f_connection/$', FConnectionView, name='f_connection'),

    path(r'^signup/$', UserCreateView.as_view(), name='signup'),
    path(r'^logout/$', login_required(logout), name='logout'),
    path(r'^profiles/(?P<username>[\w.@+-]+)/$', login_required(ProfileUpdateView.as_view()), name='profile_update'),
    path(r'^profiles/(?P<username>[\w.@+-]+)/friends/$', login_required(RelationshipListView.as_view()), name='relationship'),
    path(r'^profiles/send-request/(?P<target>\d+)/$', login_required(send_request), name='profile_send_request'),
    path(r'^profiles/request/accept/(?P<target>\d+)/$', login_required(accept_request), name='profile_accept_request'),
    path(r'^profiles/request/reject/(?P<target>\d+)/$', login_required(reject_request), name='profile_reject_request'),
    path(r'^profiles/request/delete/(?P<target>\d+)/$', login_required(delete_request), name='profile_delete_request'),

    path(r'^user/(?P<username>[\w.@+-]+)/$', login_required(ProfileDetailView.as_view()), name='profile_detail'),

    path(r'^friends/(?P<target>\d+)/delete/$', login_required(delete_friend), name='delete_friend'),
    
    path(r'^profiles/(?P<username>[\w.@+-]+)/commercial-account/$', login_required(CommercialAccountView.as_view()), name='commercial_account'),
    path(r'^p/(?P<username>[\w.@+-]+)/activate/$', ActivateAccountView.as_view(), name='activate_account'),

    
    path(r'^conditions/$', ConditionsView , name='conditions'),
    path(r'^principles/$', PrinciplesView , name='principles'),
    path(r'^politics/$', PoliticsView , name='politics'),

    path(r'^atractivos/$', TempView , name='temp'),

    #url(r'^user/profile/$', login_required(UserProfileView.as_view()), name='user_profile'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]
