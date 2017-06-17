#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/30 11:57"

configs ={
    #主机在服务端的ID
    'HostID': 1,
    #server端IP地址
    "Server": "192.168.1.105",
    #端口
    "ServerPort":8889,
    "urls":{
        #get方法获取
        'get_configs' :['api/client/config','get'],  #acquire all the services will be monitored
        #post方法发送
        'service_report': ['api/client/service/report/','post'],

    },
    #请求超时时间
    'RequestTimeout':30000,
    #更新时间
    'ConfigUpdateInterval': 300, #5 mins as default

}