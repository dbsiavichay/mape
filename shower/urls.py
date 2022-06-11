from django.urls import path, include
from .views import *

urlpatterns = [	    
    path(r'^shower/(?P<model>[\w.@+-]+)/$', ShowerListView.as_view(), name='shower'),
]