from django.conf.urls import url
from .views import *

urlpatterns = [	    
    url(r'^shower/(?P<model>[\w.@+-]+)/$', ShowerListView.as_view(), name='shower'),
]