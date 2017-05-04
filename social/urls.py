from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [        
    url(r'^$', auth_views.login, {'template_name': 'social/login.html',}, name='login'),
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    #url(r'^logout/$', logout),
    #url(r'^user/profile/$', login_required(UserProfileView.as_view()), name='user_profile'),
    #url(r'^user/profile/(?P<pk>\d+)/$', login_required(UserProfileDetailView.as_view()), name='user_profile_detail'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]