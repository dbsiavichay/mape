from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    url(r'^$', UserCreateView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', login_required(logout), name='logout'),
    url(r'^profiles/(?P<username>[\w.@+-]+)/$', login_required(ProfileUpdateView.as_view()), name='profile_update'),
    #url(r'^user/profile/$', login_required(UserProfileView.as_view()), name='user_profile'),
    #url(r'^user/profile/(?P<pk>\d+)/$', login_required(UserProfileDetailView.as_view()), name='user_profile_detail'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]
