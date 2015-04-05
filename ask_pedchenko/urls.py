from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^question', views.question),
    url(r'^login', views.login),
    url(r'^register', views.register),
    url(r'^ask', views.ask),

)
