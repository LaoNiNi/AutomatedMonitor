#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/5/1 20:07"

import subprocess


def monitor(frist_invoke=1):
    monitor_dic = {
        'SwapUsage': 'percentage',
        'MemUsage'  : 'percentage',
    }
    shell_command ="grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' /proc/meminfo"
    #状态码
    status = subprocess.call(shell_command, shell=True)
    result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.read()
    result = result.decode("utf8")
    if status != 0: #cmd exec error
        value_dic = {'status':status}
    else:
        value_dic = {'status':status}
        result = result.split('kB\n')
        result.pop()
        for i in result:
            key= i.split()[0].strip(':') # factor name
            value = i.split()[1]   # factor value
            value_dic[ key] =  value
        # print(value_dic)
        if monitor_dic['SwapUsage'] == 'percentage':
            #交换分区剩余百分比例
            value_dic['SwapUsage_p'] = str(100 - int(value_dic['SwapFree']) * 100 / int(value_dic['SwapTotal']))
        #real SwapUsage value
        value_dic['SwapUsage'] = int(value_dic['SwapTotal']) - int(value_dic['SwapFree'])

        MemUsage = int(value_dic['MemTotal']) - (int(value_dic['MemFree']) + int(value_dic['Buffers'])  + int(value_dic['Cached']))
        if monitor_dic['MemUsage'] == 'percentage':
            value_dic['MemUsage_p'] = str(int(MemUsage) * 100 / int(value_dic['MemTotal']))
        #real MemUsage value
        value_dic['MemUsage'] = MemUsage
    return value_dic

# if __name__ == '__main__':
#     print(type(monitor()),monitor())
