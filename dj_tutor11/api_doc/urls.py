# -*- coding: utf-8 -*-
# @Author: theo-l
# @Date:   2017-07-10 09:19:29
# @Last Modified by:   theo-l
# @Last Modified time: 2017-08-01 10:03:41

from django.conf.urls import url
from api_doc import views

urlpatterns = [
    # url(r'^$', views.index, name='app-list'),
    url(r'^resources/(?P<app_id>[\w-]+)/$', views.app_resource_list, name='app-resource-list'),
    url(r'^apis/(?P<app_id>[\w-]+)/(?P<resource_name>\w+)/$', views.app_resource_api_list, name='app-resource-api-list'),
    url(r'^api/(?P<api_id>[\w-]+)/$', views.app_resource_api_detail, name='app-resource-api-detail'),

    url(r'^xapi/?(?P<pk>[\w\d-]+)?/$', views.APIManagerView.as_view(), name='app-list'),


]
