from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
	
    #url(r'^event/add/comment/$', login_required(add_event_comment), name='add_event_comment'),    
    #url(r'^locality/add/comment/$', login_required(add_locality_comment), name='add_locality_comment'),    
    url(r'^comment/add/$', login_required(CommentCreateView.as_view()), name='add_comment'),    
    url(r'^comment/(?P<pk>\d+)/delete/$', login_required(CommentDeleteView.as_view()), name='delete_comment'),    
]