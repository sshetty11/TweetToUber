from django.conf.urls import url
from . import views

# Create your views here.
urlpatterns=[
    url(r'^main/', views.index, name='index'),
    url(r'^redirect/', views.redirect, name='redirect'),
    url(r'^cburl/', views.cburl, name='cburl'),
    ]
