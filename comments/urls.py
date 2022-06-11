from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [    
    path(r'^comment/add/$', login_required(CommentCreateView.as_view()), name='add_comment'),    
    path(r'^comment/(?P<pk>\d+)/delete/$', login_required(CommentDeleteView.as_view()), name='delete_comment'),    
]