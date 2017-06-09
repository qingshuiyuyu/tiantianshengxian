#coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url('^register/$',views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/$', views.register_exist),
    url(r'^info/$',views.info),
    url(r'^order(\d*)/$', views.order),
    url(r'^site/$',views.site),
    url(r'^logout/$',views.logout),
    url('^login/$',views.login),
    url(r'^login_handle/$', views.login_handle),
]
