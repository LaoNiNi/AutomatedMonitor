#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/29 11:42"
import time,threading,json

import requests

from conf import settings
from plugins import plugin_api

class ClientHandlers(object):

    def __init__(self):
        #初始化监控服务
        self.monitor_services = {}

    def load_lastest_config(self):
        """
        加载最新的配置信息
        :return:
        """
        #request请求方式api/client/config
        request_type = settings.configs["urls"]["get_configs"][1]
        #拼接url：api/client/config
        request_url = "%s/%s" % (settings.configs['urls']['get_configs'][0], settings.configs['HostID'])
        lastest_config = self.url_request(request_type,request_url)
        #把最小配置更新到监控服务字典中
        self.monitor_services.update(lastest_config)


    def forever_run(self):
        #启动客户端
        exit_flag = False
        #第一次启动时初始化最新配置时间
        config_lastest_update_time = 0
        while not exit_flag:

            if time.time() - config_lastest_update_time > settings.configs['ConfigUpdateInterval']:
                self.load_lastest_config()
                print("Lastest_config:",self.monitor_services)
                config_lastest_update_time = time.time()

            """
            Lastest_config: {'services': {'LinuxCPU': ['get_linux_cpu', 15], 'LinuxMemory': ['get_memory_info', 60],
            'LinuxNetwork': ['GetNetworkStatus', 60]}}

            """
            for service_name,val in self.monitor_services['services'].items():
                if len(val) ==2:
                    # 第一次启动插件时，初始化当前时间，给每个服务维护一个计时器
                    self.monitor_services['services'][service_name].append(0)
                #获取监控间隔和最新插件时间
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time > monitor_interval:

                    print("插件最新配置时间--->",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(last_invoke_time)),
                          "当前时间--->",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
                    #重置计时器时间
                    self.monitor_services['services'][service_name][2] = time.time()
                    t = threading.Thread(target=self.invoke_plugin,args=(service_name,val))
                    t.start()
                    print("启动监控的服务： [{ServiceName}]".format(ServiceName=service_name))

                else:
                    #需要等待监控间隔时间
                    print("监控的服务： {ServiceName} 距离下次启动时间：{interval} secs".format(ServiceName=service_name,

                                                                  interval=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(monitor_interval - (time.time() - last_invoke_time)))))
                    time.sleep(5)

        time.sleep(1)


    #运行插件
    def invoke_plugin(self,service_name,val):
        #{"services": {"LinuxNetwork": ["n/a", 60,0], "LinuxMemory": ["n/a", 60,0], "LinuxCPU": ["n/a", 60,0]}}
        #获取插件名
        plugin_name = val[0]
        if hasattr(plugin_api,plugin_name):
            func = getattr(plugin_api,plugin_name)
            plugin_callback = func()


            report_data = {
                #客户端ID
                'client_id':settings.configs['HostID'],
                #服务名
                'service_name':service_name,
                #数据
                'data':plugin_callback
            }
            print("####################################################")
            print(report_data)
            print("####################################################")
            #请求方式get or post
            request_action = settings.configs['urls']['service_report'][1]
            #请求路径
            request_url = settings.configs['urls']['service_report'][0]

            #report_data = json.dumps(report_data)
            # print('---report data（发送的数据）:',report_data)
            #调用url_request方法，以post方式发送request
            self.url_request(request_action, request_url, params=report_data)
        else:
            print("\033[31;1mCannot find service [%s]'s plugin name [%s] in plugin_api\033[0m"% (service_name,plugin_name ))
        # print('--plugin:',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(val)))
        print("该进程已执行")


    def url_request(self,action,request_url,**extra_data):

        abs_url = "http://{ip_addr}:{port}/{url}".format(ip_addr=settings.configs["Server"],
                                                         port=settings.configs["ServerPort"],
                                                         url=request_url)
        print("\033[31;1m{abs_url}\033[0m".format(abs_url=abs_url),type(extra_data),extra_data)
        if action in ('get',"GET"):
            print(abs_url,type(extra_data))
            try:
                r = requests.get(abs_url,timeout=settings.configs['RequestTimeout'])
                r_data = r.json()
                return r_data

            except requests.RequestException as E :
                exit("\033[31;1m%s\033[0m" % E)

        elif action in ('post','POST'):
            try:
                #把数据转换成json再通过post发送
                data = json.dumps(extra_data['params'])
                req = requests.post(url=abs_url,data=data)

                # res_data = req.json()
                # res_data = req.text
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" % (action, abs_url, req))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                return req

            except Exception as e:
                print('------exec', e)
                exit("\033[31;1m%s\033[0m" % e)











