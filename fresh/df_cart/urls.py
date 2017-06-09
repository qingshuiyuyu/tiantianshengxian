#coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.list),
    #url(r'^list$', views.list),
    url(r'^add(\d+)_(\d+)/$',views.add),
    url('^count_change/$', views.count_change),
    url('^delete/$', views.delete),
    url(r'^order/$',views.order),
]
