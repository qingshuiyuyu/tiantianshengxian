#coding:utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$',views.order),
    url('^pay(\d+)/$',views.pay),
]