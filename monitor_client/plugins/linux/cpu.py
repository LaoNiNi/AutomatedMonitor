#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/30 17:15"

import subprocess

def monitor(frist_invoke=1):
    shell_command = 'sar 1 3| grep "^平均时间:"'
    ret_status = subprocess.call(shell_command,shell=True)
    result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.read()
    result = result.decode("utf8")

    if ret_status != 0:
        #获取不到数据，
        value_dic = {'status':ret_status}
    else:
        value_dic = {}
        user,nice,system,iowait,steal,idle = result.split()[2:]
        value_dic = {
            "user":user,
            "nice":nice,
            "system":system,
            "iowait":iowait,
            "steal":steal,
            "idle":idle
        }


if __name__ == '__main__':
    print(monitor())