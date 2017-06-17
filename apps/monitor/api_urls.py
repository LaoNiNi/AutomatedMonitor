#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/29 16:43"

from django.conf.urls import url

from .views import client_config_view,service_data_report_view

urlpatterns = [
    #client配置信息
    url(r'^client/config/(?P<client_id>\d+)/$',client_config_view.as_view(),name='client_config'),
    #client统一汇报数据接口
    url(r'client/service/report/$',service_data_report_view,name='service_data_report'),


]

