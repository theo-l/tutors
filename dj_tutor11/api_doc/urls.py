# -*- coding: utf-8 -*-
# @Author: theo-l
# @Date:   2017-07-10 09:19:29
# @Last Modified by:   theo-l
# @Last Modified time: 2017-08-03 06:34:41

from django.conf.urls import url, include
from api_doc import views

urlpatterns = [
    # url(r'^$', views.index, name='app-list'),
    # url(r'^', include(views.APIManagerView.urls)),
    # url(r'^resources/(?P<app_id>[\w-]+)/$', views.app_resource_list, name='app-resource-list'),
    # url(r'^apis/(?P<app_id>[\w-]+)/(?P<resource_name>\w+)/$', views.app_resource_api_list, name='app-resource-api-list'),
    # url(r'^api/(?P<api_id>[\w-]+)/$', views.app_resource_api_detail, name='app-resource-api-detail'),
]
