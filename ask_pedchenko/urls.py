from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask_pedchenko.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.hello),
)
