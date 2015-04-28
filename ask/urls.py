from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^question/(?P<question_id>\d+)', views.question, name="question"),
    url(r'^login', views.login, name="login"),
    url(r'^register', views.register, name="register"),
    url(r'^ask', views.ask, name="ask"),
    url(r'^newest', views.index, {'order':'newest'}, name="newest"),
    url(r'^best', views.index, {'order':'best'}, name="best"),
)
