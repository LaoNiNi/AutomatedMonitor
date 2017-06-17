#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/29 16:34"
import traceback

from django.views.generic import View

from .models import Host


class ClientHandler(View):
    #初始化
    def __init__(self,client_id):
        self.client_id = client_id
        #client配置
        self.client_configs = {
            "services":{}
        }


    def fetch_configs(self):

        try:

            host_obj_id = Host.objects.get(id=self.client_id)
            print(">>>>>>>>>",host_obj_id)
            #获取模板list
            template_list = list(host_obj_id.templates.select_related())
            print(">>>>",template_list)
            #获取主机组obj

            # host_group_obj = host_obj_id.host_groups.select_related()
            #把主机组下的目标添加进来
            for host_group in host_obj_id.host_groups.select_related():
                template_list.extend(host_group.templates.select_related())
            print("--->",template_list)
            #获取服务列表
            for template in template_list:
                for service in template.services.select_related():
                    print(service)
                    #获取插件名和间隔时间
                    self.client_configs['services'][service.name] = [service.plugin_name,service.interval]

        except:
            traceback.print_exc()
        return self.client_configs

