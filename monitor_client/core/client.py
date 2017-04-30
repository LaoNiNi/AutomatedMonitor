#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/29 11:42"
import time,threading

import requests

from conf import settings

class ClientHandlers(object):

    def __init__(self):
        #初始化监控服务
        self.monitor_services = {}

    def load_lastest_config(self):
        """
        加载最新的配置信息
        :return:
        """
        lastest_config = self.url_request()
        self.monitor_services.update(lastest_config)


    def forever_run(self):
        #启动客户端
        exit_flag = False
        #第一次启动时初始化最新配置时间
        config_lastest_update_time = 0
        while not exit_flag:

            if time.time() - config_lastest_update_time > settings['ConfigUpdateInterval']:
                self.load_lastest_config()
                print("Lastest_config",self.monitor_services)
                config_lastest_update_time = time.time()

            for service_name,val in self.monitor_services['services'].items():
                #第一次启动插件时，初始化当前时间，给每个服务维护一个计时器
                if len(val) ==2:
                    self.monitor_services['services'][service_name].append(0)
                #获取监控间隔和最新插件时间
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time > monitor_interval:
                    print("--->",last_invoke_time,time.time())
                    #重置计时器时间
                    self.monitor_services['services'][service_name][2] = time.time()
                    t = threading.Thread(target=self.invoke_plugin,args=(service_name,val))
                    t.start()
                    print("Going to monitor [{ServiceName}]".format(ServiceName=service_name))

                else:
                    #需要等待监控间隔时间
                    print("Going to monitor [{ServiceName}] in [{interval}] secs".format(ServiceName=service_name,
                                                                  interval=monitor_interval - (time.time() - last_invoke_time)))


        time.sleep(1)
    def invoke_plugin(self,service_name,val):
        pass


    def url_request(self,**extra_data):
        #request请求方式
        request_type = settings["urls"]["get_configs"][1]
        #拼接url
        request_url = "%s/%s" % (settings.configs['urls']['get_configs'][0], settings.configs['HostID'])
        abs_url = "http://{ip_addr}:{port}/{url}".format(ip_addr=settings["Server"],
                                                         port=settings["ServerPort"],
                                                         url=request_url)
        if request_type in ('get',"GET"):
            print(abs_url,extra_data)
            try:
                r = requests.get(abs_url,timeout=settings['RequestTimeout'])
                r_data = r.json()
                return r_data

            except requests.RequestException as E :
                exit("\033[31;1m%s\033[0m" % E)

        elif request_type in ('post','POST'):
            pass









