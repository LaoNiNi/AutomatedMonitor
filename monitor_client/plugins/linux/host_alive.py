#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/5/1 3:44"


import subprocess

def monitor(frist_invoke=1):
    value_dic = {}
    shell_command = 'uptime'
    result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.read()

    #user,nice,system,iowait,steal,idle = result.split()[2:]
    value_dic= {
        'uptime': result,

        'status': 0
    }
    return value_dic


print monitor()
