#coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url('^$',views.index),
    url('^login/$',views.login),
    url('^register/$',views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/$', views.register_exist),
    url('^info',views.info),
    url('^order',views.order),
    url('^site',views.site),
]