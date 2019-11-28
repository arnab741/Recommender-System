from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name="home"

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^show/$', views.showdata, name="showdata"),
    url(r'^(?P<search>[\w\-]+)/$', views.show, name="compare"),
]